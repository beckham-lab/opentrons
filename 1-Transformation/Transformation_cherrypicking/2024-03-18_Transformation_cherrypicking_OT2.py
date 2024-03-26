
from opentrons import protocol_api
from opentrons.types import Point # for making point offsets
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

########### Description ################
# This protocol plates out competent cells into a 96-well plate then cherry picks from up to 3 plasmid plates (Twist format) for transformation.
# After an incubation period, LB media (no antibiotic) is added for an outgrowth step. 
# Then LB + antibiotic is added for overnight growth. 
# Estimated time: 1.5 h for full plate
# Tip usage: 1 rack of p300 tips

############# Setup #################
#for LB and LB+antibiotic - load 50 mL, leaves enough to pull up at end

############# Well Transfers #########
plate_1 = {'A1': 'A1', 'A5': 'A2', 'A7': 'A3'}
plate_2 = {'A1': 'D1', 'A5': 'D2', 'A7': 'D3'}
plate_3 = {'A1': 'F1', 'A5': 'F2', 'A7': 'F3'}

############## Variables #############
set_temp = 4 #C, cool temp for comp cells
competent_cell_volume = 50 #uL
plasmid_volume = 5 #ul, stocks ~10 ng/uL 

outgrowth_media_vol = 200 #uL
LB_3Xantibiotic_media_vol = 100 #uL

p300_multi_well_bottom_clearance_aspirate = 3
p300_multi_well_bottom_clearance_dispense = 30

p20_well_bottom_clearance_aspirate = 1
p20_well_bottom_clearance_dispense = 1

############# Protocol ###############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_20ul', 9, label='20uL Rack')
    pipette_P20 = protocol.load_instrument('p20_single_gen2', mount = 'right', tip_racks = [tiprack_1])

    tiprack_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 10, label='200uL Filter Rack')
    pipette_multi_300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks=[tiprack_2])

    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open('/Users/bnortonb/Documents/OT-2/Custom Labware/twist_96_wellplate_400ul_P20multitest/twist_96_wellplate_400ul.json') as labware_file:
            labware_def = json.load(labware_file)
            plasmids_plate1 = protocol.load_labware_from_definition(labware_def, 2, label = 'Plasmids Plate 1') 
            plasmids_plate2 = protocol.load_labware_from_definition(labware_def, 5, label = 'Plasmids Plate 2') 
            plasmids_plate3 = protocol.load_labware_from_definition(labware_def, 8, label = 'Plasmids Plate 3') 
    else:
        # Use the absolute file path
        plasmids_plate1 = protocol.load_labware('twist_96_wellplate_400ul', 2, label = 'Plasmids Plate 1') 
        plasmids_plate2 = protocol.load_labware('twist_96_wellplate_400ul', 5, label = 'Plasmids Plate 2') 
        plasmids_plate3 = protocol.load_labware('twist_96_wellplate_400ul', 8, label = 'Plasmids Plate 3') 
    
    temp_mod_1 = protocol.load_module('temperature module gen2', 4)
    transform_plate = temp_mod_1.load_labware('nest_96_wellplate_2ml_deep', label = 'Transformation Plate')
    
    competent_cells = protocol.load_labware('nest_12_reservoir_15ml', 1, label = 'Competent Cells')

    outgrowth_media = protocol.load_labware('nest_1_reservoir_195ml', 7, label='LB, no antibiotic')
    LB_antibiotic = protocol.load_labware('nest_1_reservoir_195ml', 6, label= 'LB + 3x antibiotic')

    pipette_multi_300.well_bottom_clearance.aspirate = p300_multi_well_bottom_clearance_aspirate
    pipette_multi_300.well_bottom_clearance.dispense = p300_multi_well_bottom_clearance_dispense
    pipette_P20.well_bottom_clearance.aspirate = p20_well_bottom_clearance_aspirate
    pipette_P20.well_bottom_clearance.dispense = p20_well_bottom_clearance_dispense

    # cool temperature modules
    temp_mod_1.start_set_temperature(set_temp)
    protocol.comment('Waiting for temp module to reach target temperature')
    temp_mod_1.await_temperature(set_temp)

    #load competent cells
    pipette_multi_300.distribute(competent_cell_volume, competent_cells['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'source well', mix_before=(3, 100))

    #transfer plasmids
    for source_well, destination_well in plate_1.items():
        pipette_P20.transfer(plasmid_volume, plasmids_plate1.wells_by_name()[source_well], transform_plate.wells_by_name()[destination_well],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_after=(2, 20))
    for source_well, destination_well in plate_2.items():
        pipette_P20.transfer(plasmid_volume, plasmids_plate2.wells_by_name()[source_well], transform_plate.wells_by_name()[destination_well],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_after=(2, 20))
    for source_well, destination_well in plate_3.items():
        pipette_P20.transfer(plasmid_volume, plasmids_plate3.wells_by_name()[source_well], transform_plate.wells_by_name()[destination_well],
        blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_after=(2, 20))
    
    #incubate cells with plasmids - 5 min
    protocol.delay(minutes=5)
    temp_mod_1.deactivate()

    #add outgrowth media
    pipette_multi_300.transfer(outgrowth_media_vol, outgrowth_media['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'destination well')
    protocol.pause('Incubate/Shake Transformation Plate for 1hr. Return plate. Fill reservoir with LB + 3xAntibiotic. Continue.')    

    #add LB + antibiotic 
    pipette_multi_300.transfer(LB_3Xantibiotic_media_vol, LB_antibiotic['A1'], transform_plate.columns(), new_tip = 'once', blow_out = True, blowout_location = 'destination well')
    
