#!/usr/bin/env python3
"""Download a datasheet PDF by searching element14 (Newark/Farnell) for the URL.

Uses the element14 Product Search API to find parts by MPN or distributor PN,
then downloads the datasheet PDF from farnell.com's CDN. PDFs download directly
without bot protection — no browser fallback needed in most cases.

Usage:
    python3 fetch_datasheet_element14.py --search <MPN_or_SKU> [--output <path>]
    python3 fetch_datasheet_element14.py <url> [--output <path>]

Exit codes:
    0 = success (PDF downloaded)
    1 = download failed after all attempts
    2 = search failed (part not found or no API key)

Environment:
    ELEMENT14_API_KEY — required for search (free from partner.element14.com)

Dependencies:
    - requests (pip install requests) — preferred
    - Falls back to urllib if requests is not installed
    - playwright (optional) — for JS-rendered datasheet pages
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

# Try to import optional dependencies; graceful fallback if not installed
try:
    import requests as _requests
except ImportError:
    _requests = None

try:
    from playwright.sync_api import sync_playwright as _sync_playwright
except ImportError:
    _sync_playwright = None


def _friendly_filename(mpn: str, description: str = "") -> str:
    """Build a human-readable filename (no extension) from MPN + description."""
    def _sanitize(s):
        s = re.sub(r'[/\\:*?"<>|,;]', "_", s)
        s = re.sub(r"\s+", "_", s)
        return re.sub(r"_+", "_", s).strip("_")

    base = _sanitize(mpn)
    if not description:
        return base
    desc = description.strip()
    if len(desc) > 80:
        desc = desc[:77].rsplit(" ", 1)[0]
    desc = _sanitize(desc)
    return f"{base}_{desc}" if desc else base


# ---------------------------------------------------------------------------
# element14 Product Search API
# ---------------------------------------------------------------------------

_DEFAULT_STORE = "www.newark.com"


def search_element14(query: str, api_key: str, store: str = _DEFAULT_STORE) -> dict | None:
    """Search element14 API for a part. Returns first match with datasheet URL.

    Accepts MPN, Newark/Farnell SKU, or keyword search terms.
    Detects the query type automatically:
      - If it looks like a numeric/alphanumeric SKU (e.g., "94AK6874"), uses id: search
      - Otherwise uses manuPartNum: search, falling back to any: keyword search
    """
    # Determine search mode
    # Newark/Farnell SKUs are typically alphanumeric codes like "94AK6874"
    # MPNs usually have dashes, longer alphanumeric strings
    query = query.strip()

    # Try MPN search first (most common case)
    result = _search_element14_raw(f"manuPartNum:{query}", api_key, store)
    if result:
        return result

    # Try as distributor SKU
    result = _search_element14_raw(f"id:{query}", api_key, store)
    if result:
        return result

    # Fall back to keyword search
    result = _search_element14_raw(f"any:{query}", api_key, store)
    return result


def _search_element14_raw(term: str, api_key: str, store: str) -> dict | None:
    """Execute a single element14 API search."""
    params = {
        "term": term,
        "storeInfo.id": store,
        "resultsSettings.offset": "0",
        "resultsSettings.numberOfResults": "5",
        "resultsSettings.responseGroup": "medium",
        "callInfo.responseDataFormat": "JSON",
        "callInfo.apiKey": api_key,
    }
    url = f"https://api.element14.com/catalog/products?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[element14] Search failed: {e}", file=sys.stderr)
        return None

    # The response key depends on the search type
    for key in ("manufacturerPartNumberSearchReturn", "keywordSearchReturn",
                "skuSearchReturn", "premierFarnellPartNumberReturn"):
        result_block = data.get(key)
        if result_block:
            break
    else:
        return None

    products = result_block.get("products", [])
    if not products:
        return None

    # Prefer exact MPN match
    query_part = term.split(":", 1)[-1].upper() if ":" in term else term.upper()
    for p in products:
        mpn = (p.get("translatedManufacturerPartNumber") or "").upper()
        sku = (p.get("sku") or "").upper()
        if mpn == query_part or sku == query_part:
            return p

    # Return first result
    return products[0]


def _get_datasheet_url(product: dict) -> str:
    """Extract the best datasheet URL from an element14 product."""
    datasheets = product.get("datasheets", [])
    for ds in datasheets:
        url = ds.get("url", "")
        if url:
            return url
    return ""


def _get_mpn(product: dict) -> str:
    """Extract MPN from product."""
    return product.get("translatedManufacturerPartNumber", "")


def _get_sku(product: dict) -> str:
    """Extract Newark/Farnell SKU from product."""
    return product.get("sku", "")


def _get_manufacturer(product: dict) -> str:
    """Extract manufacturer name from product."""
    return product.get("brandName", "")


def _get_description(product: dict) -> str:
    """Extract description from product."""
    return product.get("displayName", "")


# ---------------------------------------------------------------------------
# URL normalization
# ---------------------------------------------------------------------------

def normalize_url(url: str) -> str:
    """Normalize datasheet URL for download."""
    if url.startswith("//"):
        url = "https:" + url
    return url


# ---------------------------------------------------------------------------
# Download functions
# ---------------------------------------------------------------------------

def download_pdf(url: str, output_path: str) -> bool:
    """Download a PDF from a URL, trying multiple methods.

    Returns True if a valid PDF was downloaded.
    """
    url = normalize_url(url)

    methods = []
    if _requests is not None:
        methods.append(("requests", _download_requests))
    methods.append(("urllib", _download_urllib))
    if _sync_playwright is not None:
        methods.append(("playwright", _download_playwright))

    for name, fn in methods:
        try:
            if fn(url, output_path):
                with open(output_path, "rb") as f:
                    header = f.read(8)
                if header.startswith(b"%PDF"):
                    size = os.path.getsize(output_path)
                    print(f"Downloaded {size:,} bytes via {name}: {output_path}")
                    return True
                else:
                    os.remove(output_path)
        except Exception:
            if os.path.exists(output_path):
                os.remove(output_path)
            continue

    return False


def _download_requests(url: str, output_path: str) -> bool:
    """Download using the requests library."""
    resp = _requests.get(
        url,
        headers={"User-Agent": _USER_AGENT},
        timeout=20,
        allow_redirects=True,
    )
    resp.raise_for_status()
    if len(resp.content) == 0:
        return False
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return True


def _download_urllib(url: str, output_path: str) -> bool:
    """Download using Python urllib (fallback)."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        with open(output_path, "wb") as f:
            shutil.copyfileobj(resp, f)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0


def _download_playwright(url: str, output_path: str) -> bool:
    """Download using Playwright headless browser (last resort)."""
    with _sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            try:
                with page.expect_download(timeout=15000) as dl_info:
                    page.goto(url, timeout=15000, wait_until="domcontentloaded")
                download = dl_info.value
                download.save_as(output_path)
                return os.path.exists(output_path) and os.path.getsize(output_path) > 0
            except Exception:
                pass

            resp = page.goto(url, timeout=20000, wait_until="domcontentloaded")
            if resp is None:
                return False
            body = resp.body()
            if body and body[:4] == b"%PDF":
                with open(output_path, "wb") as f:
                    f.write(body)
                return True
            return False
        finally:
            page.close()
            browser.close()


def try_alternative_sources(mpn: str, output_path: str) -> bool:
    """Try alternative datasheet sources when element14 URL fails."""
    alternatives = []
    mpn_upper = mpn.upper()

    # Microchip direct URL pattern
    if any(x in mpn_upper for x in ("ATMEGA", "ATTINY", "PIC", "SAMD", "SAM")):
        alternatives.append(
            f"https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/{mpn}-DataSheet.pdf"
        )

    for alt_url in alternatives:
        if download_pdf(alt_url, output_path):
            return True

    return False


# ---------------------------------------------------------------------------
# PDF verification
# ---------------------------------------------------------------------------

def _extract_pdf_text(pdf_path: str, max_pages: int = 3) -> str:
    """Extract text from the first few pages of a PDF."""
    try:
        result = subprocess.run(
            ["pdftotext", "-l", str(max_pages), pdf_path, "-"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        with open(pdf_path, "rb") as f:
            raw = f.read(200_000)
        strings = re.findall(rb"[\x20-\x7e]{4,}", raw)
        return " ".join(s.decode("ascii", errors="ignore") for s in strings)
    except Exception:
        return ""


def verify_datasheet(
    pdf_path: str,
    mpn: str,
    description: str = "",
    manufacturer: str = "",
) -> dict:
    """Verify a downloaded PDF is the correct datasheet."""
    text = _extract_pdf_text(pdf_path)
    if not text or len(text) < 50:
        return {
            "verified": False, "confidence": "unverified",
            "mpn_found": False, "manufacturer_found": False,
            "keyword_hits": 0, "keyword_total": 0,
            "details": "Could not extract text from PDF",
        }

    text_upper = text.upper()
    mpn_upper = mpn.upper()
    mpn_found = mpn_upper in text_upper

    if not mpn_found:
        base_mpn = re.sub(
            r"(DRLR|DRL|DGKR|DGK|DCKR|DCK|DBVR|DBV|PWPR|PWP|RGER|RGE|"
            r"RGTR|RGT|NRND|TR|CT|ND|LT1G|LT3G|BK|PBF|-ND)$",
            "", mpn_upper,
        )
        if base_mpn and len(base_mpn) >= 4 and base_mpn != mpn_upper:
            mpn_found = base_mpn in text_upper

    mfg_found = False
    if manufacturer:
        mfg_upper = manufacturer.upper()
        mfg_found = mfg_upper in text_upper
        if not mfg_found:
            first_word = mfg_upper.split()[0] if " " in mfg_upper else ""
            if first_word and len(first_word) >= 4:
                mfg_found = first_word in text_upper

    keywords = []
    if description:
        skip = {"the", "a", "an", "for", "and", "or", "with", "in", "to",
                "of", "at", "by", "on", "no", "w", "smd", "smt"}
        for word in re.split(r"[\s/,_-]+", description):
            w = word.strip().upper()
            if len(w) >= 3 and w not in skip and not re.match(r"^\d+$", w):
                keywords.append(w)

    keyword_hits = sum(1 for kw in keywords if kw in text_upper) if keywords else 0
    keyword_total = len(keywords)

    if mpn_found:
        confidence = "verified"
        details = f"MPN '{mpn}' found in PDF text"
    elif mfg_found and keyword_hits >= max(1, keyword_total // 2):
        confidence = "likely"
        details = (f"MPN not found but manufacturer '{manufacturer}' present "
                   f"with {keyword_hits}/{keyword_total} description keywords")
    elif keyword_hits >= max(2, keyword_total * 2 // 3):
        confidence = "likely"
        details = f"{keyword_hits}/{keyword_total} description keywords found"
    elif keyword_hits == 0 and keyword_total >= 3 and not mfg_found:
        confidence = "wrong"
        details = (f"No MPN, manufacturer, or description keywords found in PDF "
                   f"(0/{keyword_total} keywords)")
    else:
        confidence = "unverified"
        details = (f"MPN not found; {keyword_hits}/{keyword_total} keywords, "
                   f"manufacturer {'found' if mfg_found else 'not found'}")

    return {
        "verified": mpn_found, "confidence": confidence,
        "mpn_found": mpn_found, "manufacturer_found": mfg_found,
        "keyword_hits": keyword_hits, "keyword_total": keyword_total,
        "details": details,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download a datasheet PDF via element14 (Newark/Farnell)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("url", nargs="?", help="Direct URL to the PDF")
    group.add_argument("--search", metavar="QUERY",
                       help="Search by MPN or Newark/Farnell part number")
    parser.add_argument("--output", "-o", help="Output file path (default: <MPN>.pdf)")
    parser.add_argument("--store", default=_DEFAULT_STORE,
                        help=f"element14 store ID (default: {_DEFAULT_STORE})")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    if args.search:
        api_key = os.environ.get("ELEMENT14_API_KEY", "")
        if not api_key:
            if args.json:
                json.dump({"success": False, "error": "ELEMENT14_API_KEY not set"}, sys.stdout)
            else:
                print("Error: ELEMENT14_API_KEY environment variable not set", file=sys.stderr)
                print("Get a free key at https://partner.element14.com/member/register",
                      file=sys.stderr)
            sys.exit(2)

        product = search_element14(args.search, api_key, args.store)
        if not product:
            if args.json:
                json.dump({"success": False, "error": "Part not found on element14"},
                          sys.stdout)
            else:
                print(f"No element14 results for '{args.search}'", file=sys.stderr)
            sys.exit(2)

        mpn = _get_mpn(product)
        sku = _get_sku(product)
        desc = _get_description(product)
        mfg = _get_manufacturer(product)
        ds_url = _get_datasheet_url(product)

        display_pn = mpn or sku or args.search
        output_path = args.output or (_friendly_filename(display_pn, desc) + ".pdf")

        if args.json:
            result = {
                "mpn": mpn,
                "sku": sku,
                "manufacturer": mfg,
                "description": desc,
                "datasheet_url": ds_url,
            }

        if not ds_url:
            print(f"No datasheet URL for {display_pn}", file=sys.stderr)
            if args.json:
                result["success"] = False
                result["error"] = "No datasheet URL in element14 listing"
                json.dump(result, sys.stdout)
            sys.exit(2)

        print(f"Downloading datasheet for {display_pn} ({sku})...", file=sys.stderr)
        if download_pdf(ds_url, output_path):
            vr = verify_datasheet(output_path, mpn or sku, desc, mfg)
            if vr["confidence"] == "wrong":
                print(f"WARNING: Downloaded PDF may be wrong datasheet for {display_pn}",
                      file=sys.stderr)
                print(f"  {vr['details']}", file=sys.stderr)
            if args.json:
                result["success"] = True
                result["output"] = output_path
                result["verification"] = vr
                json.dump(result, sys.stdout)
            sys.exit(0)

        # Try alternative sources
        if mpn:
            print(f"element14 URL failed, trying alternatives for {mpn}...",
                  file=sys.stderr)
            if try_alternative_sources(mpn, output_path):
                vr = verify_datasheet(output_path, mpn, desc, mfg)
                if args.json:
                    result["success"] = True
                    result["output"] = output_path
                    result["source"] = "alternative"
                    result["verification"] = vr
                    json.dump(result, sys.stdout)
                sys.exit(0)

        print(f"Failed to download datasheet for {display_pn}", file=sys.stderr)
        if args.json:
            result["success"] = False
            result["error"] = "All download methods failed"
            json.dump(result, sys.stdout)
        sys.exit(1)

    else:
        # Direct URL mode
        url = args.url
        output_path = args.output or "datasheet.pdf"

        if download_pdf(url, output_path):
            if args.json:
                json.dump({"success": True, "output": output_path, "url": url}, sys.stdout)
            sys.exit(0)
        else:
            print(f"Failed to download PDF from {url}", file=sys.stderr)
            if args.json:
                json.dump({"success": False, "url": url, "error": "Download failed"},
                          sys.stdout)
            sys.exit(1)


if __name__ == "__main__":
    main()
