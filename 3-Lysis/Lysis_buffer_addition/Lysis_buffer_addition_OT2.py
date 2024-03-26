from opentrons import protocol_api
from opentrons.types import Point # for making point offsets
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

#for simulate, modify path
custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/Protocol_code/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json'

########### Description ################
# After cells are pelleted via centrifugation, this protocol adds 1.5 mL of lysis buffer to each well in 4 24-well plates.
# Estimated time: 20 min
# Tip usage: 1 column of p300 tips

########### Variables #################
volume_lysis_buffer = 1500/2 #uL, half because using two tips per dispense 
                            #need 200 mL, fill two reservoirs each with 100 mL (wash buffer + 1% detergent + DNase + Lysozyme) and this leaves enough for aspirating

pipette_height_dispense = 25 # to keep tip clean between buffers
pipette_height_aspirate_buffer = 3 #mm, prevents it from hitting the bottom

pipette_y_offset = 5.5 #offsets multichannel so two tips go into each well of the 24 well plates

def run(protocol: protocol_api.ProtocolContext):

    ######################### Load Labware #####################################
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 10, label='300uL Rack')

    pipette_multi_P300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1])

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
    
    lysis_buffer1 = protocol.load_labware('nest_1_reservoir_195ml', 7, label = 'Lysis Buffer 1') 
    lysis_buffer2 = protocol.load_labware('nest_1_reservoir_195ml', 4, label = 'Lysis Buffer 2') 

    #Load Lysis Buffer
    pipette_multi_P300.well_bottom_clearance.aspirate = pipette_height_aspirate_buffer
    pipette_multi_P300.well_bottom_clearance.dispense = pipette_height_dispense

    column_names = ['A1','A2','A3','A4','A5','A6'] #24 well plate, 6 columns
    pipette_multi_P300.pick_up_tip()
    for column_name in column_names:
        pipette_multi_P300.transfer(volume_lysis_buffer, lysis_buffer1.wells_by_name()['A1'], cell_culture_plateA.wells_by_name()[column_name].top().move(Point(0, pipette_y_offset, 0)),
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
    for column_name in column_names:
        pipette_multi_P300.transfer(volume_lysis_buffer, lysis_buffer1.wells_by_name()['A1'], cell_culture_plateB.wells_by_name()[column_name].top().move(Point(0, pipette_y_offset, 0)),
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
    for column_name in column_names:
        pipette_multi_P300.transfer(volume_lysis_buffer, lysis_buffer2.wells_by_name()['A1'], cell_culture_plateC.wells_by_name()[column_name].top().move(Point(0, pipette_y_offset, 0)),
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
    for column_name in column_names:
        pipette_multi_P300.transfer(volume_lysis_buffer, lysis_buffer2.wells_by_name()['A1'], cell_culture_plateD.wells_by_name()[column_name].top().move(Point(0, pipette_y_offset, 0)),
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
    pipette_multi_P300.drop_tip()
    