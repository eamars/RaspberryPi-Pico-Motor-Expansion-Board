# Steps to make the controller board with JLCPCB

This document will show you how to order the PCB from JLCPCB step by step. 

## Files under production directory

* GERBER-pico_expansion_board.zip: PCB Gerber file, used for PCB manufacturing.

* BOM-pico_expansion_board.csv: BOM (Bill of Material) file used to order PCBA (PCB Assembly) service from JLCPCB

* CPL-pico_expansion_board.csv: Component placement coordinate file used to order PCBA service from JLCPCB.

* LCSC_Bom.csv: BOM file used to order components yourself from LCSC (Component stockist for JLCPCB). 

* jlcpcb_to_lcsc_bom.py: Python script to generate `LCSC_Bom.csv` from `BOM-pico_expansion_board.csv`. NOT USED FOR PRODUCTION. 

## Order PCB

1. Select Instant Quote from https://jlcpcb.com/

2. Select `GERBER-pico_expansion_board.zip` after clicking "Add gerber file"

3. Select the colour of PCB you like, leave all other settings default, then click "SAVE TO CART".

## Order PCBA

1. Select PCB Assembly after step 2 from above section. 

2. Select number of boards to be assembled

3. Select "Yes" for "Cofnirm Parts Placement" option. 

4. Click "Confirm"

5. For "Bill of Materials" page, select NEXT, then you will be prompted to add BOM file and CPL file. 

6. Upload `BOM-pico_expansion_board.csv` for "Add BOM File" and `CPL-pico_expansion_board.csv` for "Add CPL File", select "Process BoM & CPL" button.

7. You will be prompted to review all cmponents and its corresponding prices. Select "NEXT" to continue. 

8. Check the component placements by comparing the preview with the Kicad PCB design. Make sure all component layouts are correct. Then select "NEXT" to continue. 

9. Select "SAVE TO CART" after reviewing the total cost. 

## Order components from LCSC

If you decide to solder the board by sourcing components yourself, then you can order all parts from LCSC by provided BOM file. 

1. Select "BOM Tool" from https://www.lcsc.com/

2. Upload `LCSC_Bom.csv` .

3. Match column name to the corresponding column type. Though the CSV column names are already modified to match the column type, you will need to match them manually from the web. Please fill all coumn types. 

4. Check the availability. Please talk to the author for substitution if any components is out of stock. 

5. Select "Add to Cart" to place the order. 


