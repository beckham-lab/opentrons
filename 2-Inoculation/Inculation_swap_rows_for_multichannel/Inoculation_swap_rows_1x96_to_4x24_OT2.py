from opentrons import protocol_api
import json
from opentrons.types import Point # for making point offsets
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

#for simulate, modify path
custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/Protocol_code/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json'

########### Description ################
# After transformation, this protocol inoculates 4 24-well plates containing media from 1 96-well plate containing transformed cells.
# Estimated time: 11 min
# Tip usage: 2 racks of half-loaded p200 filter tips

############## Variables #############

inoculation_volume = 20 #uL
    
p300_well_bottom_clearance_aspirate = 2 #mm
p300_well_bottom_clearance_dispense = 5 #mm

pipette_y_offset = -9 #applied to quadrant C and D to pull from B1-B6 (for C) and B7-B12 (for D)

aspiration_speed  = 300
dispense_speed = 300

############## Load Labware #############

def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 7, label='HALF LOADED - 200uL Filter Rack')
    tiprack_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4, label='HALF LOADED - 200uL Filter Rack')
    pipette_multi_P300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks=[tiprack_1,tiprack_2])
    
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

    overnight_cultures = protocol.load_labware('nest_96_wellplate_2ml_deep', 10, label = 'Overnight Cultures Plate')
   
    pipette_multi_P300.well_bottom_clearance.aspirate = p300_well_bottom_clearance_aspirate
    pipette_multi_P300.well_bottom_clearance.dispense = p300_well_bottom_clearance_dispense

############## Protocol #############

    source_wells_A = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    source_wells_B = ['A7','A8','A9','A10','A11','A12']
    source_wells_C = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    source_wells_D = ['A7','A8','A9','A10','A11','A12']

    destination_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    
    pipette_multi_P300.flow_rate.aspirate = aspiration_speed
    pipette_multi_P300.flow_rate.dispense = dispense_speed

    pipette_multi_P300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in source_wells_A], [cell_culture_plateA.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100), trash=False)


    pipette_multi_P300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well] for well in source_wells_B], [cell_culture_plateB.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100), trash=False)
    

    pipette_multi_P300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well].bottom().move(Point(0,pipette_y_offset,0)) for well in source_wells_C], [cell_culture_plateC.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100), trash=False)


    pipette_multi_P300.transfer(inoculation_volume, [overnight_cultures.wells_by_name()[well].bottom().move(Point(0,pipette_y_offset,0)) for well in source_wells_D], [cell_culture_plateD.wells_by_name()[well] for well in destination_wells],
    blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100), trash=False)



  