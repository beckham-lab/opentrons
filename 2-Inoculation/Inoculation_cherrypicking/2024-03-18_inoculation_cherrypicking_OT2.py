
from opentrons import protocol_api
from opentrons.types import Point # for making point offsets
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

########### Description ################
# After transformation, this protocol inoculates 4 24-well plates containing media from 1 96-well plate containing transformed cells.
# Estimated time: 1 h
# Tip usage: 1 rack of p300 tips

############## Variables #############
inoculation_volume = 20 #uL

p300_well_bottom_clearance_aspirate = 2
p300_well_bottom_clearance_dispense = 2

############# Protocol ###############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1, label='200uL Filter Rack')
    pipette_300 = protocol.load_instrument('p300_single_gen2', mount = 'left', tip_racks=[tiprack_1])
    

    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open('/Users/bnortonb/Documents/Automation_paper/Protocol_code/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json') as labware_file:
            labware_def = json.load(labware_file)
            cell_culture_plateA = protocol.load_labware_from_definition(labware_def, 8, label = 'Cell Culture Plate A')
            cell_culture_plateB = protocol.load_labware_from_definition(labware_def, 9, label = 'Cell Culture Plate B')
            cell_culture_plateC = protocol.load_labware_from_definition(labware_def, 5, label = 'Cell Culture Plate C')
            cell_culture_plateD = protocol.load_labware_from_definition(labware_def, 6, label = 'Cell Culture Plate D')
    else:
        # Use the absolute file path
        cell_culture_plateA = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul', 8, label = 'Cell Culture Plate A') 
        cell_culture_plateB = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul', 9, label = 'Cell Culture Plate B') 
        cell_culture_plateC = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul', 5, label = 'Cell Culture Plate C') 
        cell_culture_plateD = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul', 6, label = 'Cell Culture Plate D')

    sourceplate1 = protocol.load_labware('nest_96_wellplate_2ml_deep', 10, label = 'Source Plate 1')
    sourceplate2 = protocol.load_labware('nest_96_wellplate_2ml_deep', 7, label = 'Source Plate 2')
    sourceplate3 = protocol.load_labware('nest_96_wellplate_2ml_deep', 4, label = 'Source Plate 3')
   
    pipette_300.well_bottom_clearance.aspirate = p300_well_bottom_clearance_aspirate
    pipette_300.well_bottom_clearance.dispense = p300_well_bottom_clearance_dispense
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['F10'], cell_culture_plateA.wells_by_name()['A1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D11'], cell_culture_plateA.wells_by_name()['A2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D1'], cell_culture_plateA.wells_by_name()['A3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['G1'], cell_culture_plateA.wells_by_name()['A4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['F8'], cell_culture_plateA.wells_by_name()['A5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['H4'], cell_culture_plateA.wells_by_name()['A6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['C7'], cell_culture_plateA.wells_by_name()['B1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['G10'], cell_culture_plateA.wells_by_name()['B2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['B8'], cell_culture_plateA.wells_by_name()['B3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['F12'], cell_culture_plateA.wells_by_name()['B4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['G3'], cell_culture_plateA.wells_by_name()['B5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D4'], cell_culture_plateA.wells_by_name()['B6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['H3'], cell_culture_plateA.wells_by_name()['C1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D2'], cell_culture_plateA.wells_by_name()['C2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['A7'], cell_culture_plateA.wells_by_name()['C3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['A10'], cell_culture_plateA.wells_by_name()['C4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['B10'], cell_culture_plateA.wells_by_name()['C5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D9'], cell_culture_plateA.wells_by_name()['C6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C2'], cell_culture_plateA.wells_by_name()['D1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['A9'], cell_culture_plateA.wells_by_name()['D2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['F3'], cell_culture_plateA.wells_by_name()['D3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['H2'], cell_culture_plateA.wells_by_name()['D4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['E8'], cell_culture_plateA.wells_by_name()['D5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C10'], cell_culture_plateA.wells_by_name()['D6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D8'], cell_culture_plateB.wells_by_name()['A1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['E4'], cell_culture_plateB.wells_by_name()['A2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['G8'], cell_culture_plateB.wells_by_name()['A3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['G2'], cell_culture_plateB.wells_by_name()['A4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['A8'], cell_culture_plateB.wells_by_name()['A5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['D7'], cell_culture_plateB.wells_by_name()['A6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['E9'], cell_culture_plateB.wells_by_name()['B1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['C1'], cell_culture_plateB.wells_by_name()['B2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['B2'], cell_culture_plateB.wells_by_name()['B3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['F2'], cell_culture_plateB.wells_by_name()['B4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['A12'], cell_culture_plateB.wells_by_name()['B5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate1.wells_by_name()['B12'], cell_culture_plateB.wells_by_name()['B6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['H1'], cell_culture_plateB.wells_by_name()['C1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['E10'], cell_culture_plateB.wells_by_name()['C2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C3'], cell_culture_plateB.wells_by_name()['C3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['B11'], cell_culture_plateB.wells_by_name()['C4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['B4'], cell_culture_plateB.wells_by_name()['C5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['B1'], cell_culture_plateB.wells_by_name()['C6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['B3'], cell_culture_plateB.wells_by_name()['D1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['A3'], cell_culture_plateB.wells_by_name()['D2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['E12'], cell_culture_plateB.wells_by_name()['D3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['D10'], cell_culture_plateB.wells_by_name()['D4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['A11'], cell_culture_plateB.wells_by_name()['D5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C8'], cell_culture_plateB.wells_by_name()['D6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C12'], cell_culture_plateC.wells_by_name()['A1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['G4'], cell_culture_plateC.wells_by_name()['A2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['G11'], cell_culture_plateC.wells_by_name()['A3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['G7'], cell_culture_plateC.wells_by_name()['A4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['E11'], cell_culture_plateC.wells_by_name()['A5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C11'], cell_culture_plateC.wells_by_name()['A6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['B7'], cell_culture_plateC.wells_by_name()['B1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E1'], cell_culture_plateC.wells_by_name()['B4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G12'], cell_culture_plateC.wells_by_name()['B5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['B10'], cell_culture_plateC.wells_by_name()['B6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G5'], cell_culture_plateC.wells_by_name()['C1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['F5'], cell_culture_plateC.wells_by_name()['C2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G10'], cell_culture_plateC.wells_by_name()['C3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['H10'], cell_culture_plateC.wells_by_name()['C4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G9'], cell_culture_plateC.wells_by_name()['C5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['D5'], cell_culture_plateC.wells_by_name()['C6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['C10'], cell_culture_plateC.wells_by_name()['D1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G8'], cell_culture_plateC.wells_by_name()['D2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['B12'], cell_culture_plateC.wells_by_name()['D3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['D10'], cell_culture_plateC.wells_by_name()['D4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E10'], cell_culture_plateC.wells_by_name()['D5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['B6'], cell_culture_plateC.wells_by_name()['D6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['E2'], cell_culture_plateD.wells_by_name()['A1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['F1'], cell_culture_plateD.wells_by_name()['A2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['C6'], cell_culture_plateD.wells_by_name()['A3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['B9'], cell_culture_plateD.wells_by_name()['A4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['H11'], cell_culture_plateD.wells_by_name()['A5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate2.wells_by_name()['D12'], cell_culture_plateD.wells_by_name()['A6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['C7'], cell_culture_plateD.wells_by_name()['B1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['A6'], cell_culture_plateD.wells_by_name()['B2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['H12'], cell_culture_plateD.wells_by_name()['B3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['H7'], cell_culture_plateD.wells_by_name()['B4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E5'], cell_culture_plateD.wells_by_name()['B5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['F8'], cell_culture_plateD.wells_by_name()['B6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['F7'], cell_culture_plateD.wells_by_name()['C1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['D9'], cell_culture_plateD.wells_by_name()['C2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E6'], cell_culture_plateD.wells_by_name()['C3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['A9'], cell_culture_plateD.wells_by_name()['C4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E7'], cell_culture_plateD.wells_by_name()['C5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['D7'], cell_culture_plateD.wells_by_name()['C6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['E8'], cell_culture_plateD.wells_by_name()['D1'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G6'], cell_culture_plateD.wells_by_name()['D2'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G7'], cell_culture_plateD.wells_by_name()['D3'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['B9'], cell_culture_plateD.wells_by_name()['D4'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['D6'], cell_culture_plateD.wells_by_name()['D5'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
    pipette_300.transfer(inoculation_volume, sourceplate3.wells_by_name()['G11'], cell_culture_plateD.wells_by_name()['D6'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))