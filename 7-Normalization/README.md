# Concentration Normalization

This OT-2 protocol uses a single channel pipette to dilute each well of the purified protein plate to the desired concentration(s). An Excel template is provided to import the starting concentrations. This protocol requires a p1000 single channel pipette and a p300 single channel pipette.

## Set-up:
1. Run *Calculate_Volumes_to_Normalize.py* 
    
    This script imports the Normalization_input.xlsx file that must contain your concentrations measured via BCA assay.

    It generates a list of wells and dilution volumes.

    It splits the list based on expression level:
    
    - high-expressing, target concentration 0.3 mg/mL
    
    - med-expressing, target concentration 0.1 mg/mL
    
    - low/non-expressing, target concentration unchanged
    
    It generates a protocol for the OT2 to add the volumes to each well.

## Notes:
To use simulate, modify the custom labware path in the script. 