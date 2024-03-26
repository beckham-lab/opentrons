from opentrons import protocol_api
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

#for simulate, modify path
custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/Protocol_code/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json'

########### Description ################
# After lysis & MagBead binding, this protocol removes the supernatant from a single 24-well plate and leaves behind the MagBeads.
# Then 300 uL of Wash Buffer is added as the first wash in the purification. 
# Estimated time: 7.5 min
# Tip usage: 7 columns of 300 uL tips

########### Variables ################ß
volume_lysis_buffer_remove = 1800/2 #uL, half because two tips per well
pipette_x_offset = 2 #to pull from off center of the MagBeads
pipette_y_offset = 5.5 #to align two tips per well

volume_wash1 = 150 #uL, half because two tips per well
                            
pipette_height_aspirate_lysis = 0
pipette_height_dispense = 20 # to keep tip clean between buffers
pipette_height_aspirate_reservoirs = 3 #mm, prevents it from hitting the bottom

########### Protocol ################
def run(protocol: protocol_api.ProtocolContext):

    ######################### Load Labware #####################################
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 9, label='300uL Rack')
    pipette_multi_P300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1])   
    mag_module = protocol.load_module('magnetic module gen2', 1)

    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open(custom_labware_file_path) as labware_file:
            labware_def = json.load(labware_file)
            mag_plate = mag_module.load_labware_from_definition(labware_def, 4)
    else:
        # Use the absolute file path
        mag_plate = mag_module.load_labware('thomsoninstrument_24_wellplate_10400ul', label = 'Plate on Mag Mod')
        
    mag_plate.set_offset(x=3, y=5.5, z=2)

    waste = protocol.load_labware('nest_1_reservoir_195ml', 3, label = 'Waste') 
    wash_buffer = protocol.load_labware('nest_1_reservoir_195ml', 6, label = 'Wash Buffer') 

    pipette_multi_P300.well_bottom_clearance.dispense = pipette_height_dispense

    mag_module.engage(height_from_base=4)

    pipette_multi_P300.pick_up_tip()
    
    column_names = ['A1','A2','A3','A4','A5','A6'] #24 well plate, 6 columns
    for column_name in column_names:
        pipette_multi_P300.well_bottom_clearance.aspirate = pipette_height_aspirate_lysis
        pipette_multi_P300.transfer(volume_lysis_buffer_remove, mag_plate.wells_by_name()[column_name], waste.wells_by_name()['A1'],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
        pipette_multi_P300.drop_tip()
        pipette_multi_P300.pick_up_tip()
        pipette_multi_P300.well_bottom_clearance.aspirate = pipette_height_aspirate_reservoirs
        pipette_multi_P300.transfer(volume_wash1, wash_buffer.wells_by_name()['A1'], mag_plate.wells_by_name()[column_name],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')

    pipette_multi_P300.drop_tip()



        