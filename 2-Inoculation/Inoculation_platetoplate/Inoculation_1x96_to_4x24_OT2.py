from opentrons import protocol_api
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

#for simulate, modify path
custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/opentrons/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json'

########### Description ################
# After transformation, this protocol inoculates 4 24-well plates containing media from 1 96-well plate containing transformed cells.
# Estimated time: 1 h
# Tip usage: 1 rack of p300 tips

############## Variables #############

inoculation_volume = 20 #uL
    
p300_well_bottom_clearance_aspirate = 2
p300_well_bottom_clearance_dispense = 2

############## Protocol #############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1, label='200uL Filter Rack')
    pipette_300 = protocol.load_instrument('p300_single_gen2', mount = 'left', tip_racks=[tiprack_1])
    
    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open(custom_labware_file_path) as labware_file:
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

    overnight_cultures = protocol.load_labware('nest_96_wellplate_2ml_deep', 10, label = 'Starter Cultures Plate')
   
    pipette_300.well_bottom_clearance.aspirate = p300_well_bottom_clearance_aspirate
    pipette_300.well_bottom_clearance.dispense = p300_well_bottom_clearance_dispense

#inoculate by quadrant
    quadrantA = ['A1','A2','A3','A4','A5','A6',
                'B1','B2','B3','B4','B5','B6',
                'C1','C2','C3','C4','C5','C6',
                'D1','D2','D3','D4','D5','D6']
    quadrantB = ['A7','A8','A9','A10','A11','A12',
                'B7','B8','B9','B10','B11','B12',
                'C7','C8','C9','C10','C11','C12',
                'D7','D8','D9','D10','D11','D12']
    quadrantC = ['E1','E2','E3','E4','E5','E6',
                'F1','F2','F3','F4','F5','F6',
                'G1','G2','G3','G4','G5','G6',
                'H1','H2','H3','H4','H5','H6',]
    quadrantD = ['E7','E8','E9','E10','E11','E12',
                'F7','F8','F9','F10','F11','F12',
                'G7','G8','G9','G10','G11','G12',
                'H7','H8','H9','H10','H11','H12']
    destination_wells = ['A1','A2','A3','A4','A5','A6',
                'B1','B2','B3','B4','B5','B6',
                'C1','C2','C3','C4','C5','C6',
                'D1','D2','D3','D4','D5','D6']

    pipette_300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in quadrantA], [cell_culture_plateA.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))

    pipette_300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in quadrantB], [cell_culture_plateB.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
   
    pipette_300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in quadrantC], [cell_culture_plateC.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))
   
    pipette_300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in quadrantD], [cell_culture_plateD.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))

  