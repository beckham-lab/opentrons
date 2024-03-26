from opentrons import protocol_api
from opentrons.types import Point # for making point offsets
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

#for simulate, modify path
custom_labware_file_path = '/Users/bnortonb/Documents/OT-2/Custom Labware/twist_96_wellplate_400ul_P20multitest/twist_96_wellplate_400ul.json'

########### Description ################
# This protocol plates out competent cells into a 96-well plate then transfers from a single plasmid plate (Twist format) for transformation.
# After an incubation period, LB media (no antibiotic) is added for an outgrowth step. 
# Then LB + antibiotic is added for overnight growth. 
# Estimated time: 
# Tip usage: 1 rack of p300 tips

############# Setup #################
#for LB and LB+antibiotic - load 50 mL, leaves enough to pull up at end

############# Well Transfers #########

plasmid_plate_columns = [0,1,2,3,4,5,6,7,8,9,10]

############## Variables #############
set_temp = 4 #C, cool temp for comp cells
competent_cell_volume = 50 #uL
plasmid_volume = 5 #ul, stocks ~10 ng/uL 

outgrowth_media_vol = 200 #uL
LB_antibiotic_media_vol = 100 #uL

p300_multi_well_bottom_clearance_aspirate = 3
p300_multi_well_bottom_clearance_dispense = 30

p20_well_bottom_clearance_aspirate = 1
p20_well_bottom_clearance_dispense = 1

############# Protocol ###############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_20ul', 9, label='20uL Rack')
    pipette_multi_20 = protocol.load_instrument('p20_multi_gen2', mount = 'right', tip_racks = [tiprack_1])

    tiprack_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 10, label='200uL Filter Rack')
    pipette_multi_300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks=[tiprack_2])
    
    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open(custom_labware_file_path) as labware_file:
            labware_def = json.load(labware_file)
            plasmids_plate = protocol.load_labware_from_definition(labware_def, 2, label='Plasmids Plate')
    else:
        # Use the absolute file path
        plasmids_plate = protocol.load_labware('twist_96_wellplate_400ul', 2, label = 'Plasmids Plate')
    
    temp_mod_1 = protocol.load_module('temperature module gen2', 4)
    transform_plate = temp_mod_1.load_labware('nest_96_wellplate_2ml_deep', label = 'Transformation Plate')
    
    competent_cells = protocol.load_labware('nest_12_reservoir_15ml', 1, label = 'Competent Cells')

    outgrowth_media = protocol.load_labware('nest_1_reservoir_195ml', 7, label='LB, no antibiotic')
    LB_antibiotic = protocol.load_labware('nest_1_reservoir_195ml', 6, label= 'LB + 3x antibiotic')

    pipette_multi_300.well_bottom_clearance.aspirate = p300_multi_well_bottom_clearance_aspirate
    pipette_multi_300.well_bottom_clearance.dispense = p300_multi_well_bottom_clearance_dispense
    pipette_multi_20.well_bottom_clearance.aspirate = p20_well_bottom_clearance_aspirate
    pipette_multi_20.well_bottom_clearance.dispense = p20_well_bottom_clearance_dispense

    # cool temperature modules
    temp_mod_1.start_set_temperature(set_temp)
    protocol.comment('Waiting for temp module to reach target temperature')
    temp_mod_1.await_temperature(set_temp)

    #load competent cells
    pipette_multi_300.distribute(competent_cell_volume, competent_cells['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'source well', mix_before=(3, 100))

    #transfer plasmids
    pipette_multi_20.transfer(plasmid_volume, [plasmids_plate.columns()[column] for column in plasmid_plate_columns], [transform_plate.columns()[column] for column in plasmid_plate_columns],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_after=(2, 20))

    # incubate cells with plasmids - 5 min
    protocol.delay(minutes=5)
    temp_mod_1.deactivate()

    #add outgrowth media
    pipette_multi_300.transfer(outgrowth_media_vol, outgrowth_media['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'destination well')
    protocol.pause('Incubate/Shake Transformation Plate for 1hr. Return plate. Fill reservoir with LB + 3xAntibiotic. Continue.')    

    #add LB + antibiotic 
    pipette_multi_300.transfer(LB_antibiotic_media_vol, LB_antibiotic['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'destination well')
    