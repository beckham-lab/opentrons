
from opentrons import protocol_api

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

############# Description ###############
# This protocol normalizes the enzyme concentrations.  
# Estimated time: 15-20 min
# Tip usage: 1 p1000 tip, 1 p300 tip

######################## Volumes for Normalizations ########################
well_volume_dict_p1000 = {'A5': 670.6, 'A7': 606.3, 'B8': 353.6, 'B10': 665.1, 'B11': 411.3, 'B12': 354.8, 'C2': 1453.4, 'C6': 539.0, 'C7': 637.4, 'C9': 627.0, 'C10': 312.1, 'C11': 505.9, 'D2': 473.1, 'D10': 658.2, 'D12': 373.3, 'E4': 329.5, 'E5': 792.7, 'E9': 692.8, 'E10': 449.4, 'F1': 588.0, 'F5': 318.7, 'F8': 647.8, 'F9': 723.9, 'F10': 450.5, 'G9': 568.2, 'G12': 426.3, 'H1': 591.6, 'H2': 1392.3, 'H3': 354.6, 'H9': 630.5, 'H10': 1163.4, 'H12': 1402.1}
well_volume_dict_p300 = {'A2': 35.1, 'A9': 87.2, 'A11': 76.8, 'B5': 35.1, 'B6': 110.5, 'C5': 121.2, 'D4': 290.0, 'D6': 150.0, 'D9': 49.1, 'E2': 81.8, 'E12': 35.3, 'F3': 139.2, 'F4': 31.5, 'F6': 110.5, 'F12': 215.2, 'G1': 53.0, 'G3': 60.2, 'G6': 99.7, 'H6': 279.2}


############################## Variables ###################################

pipette_height_dispense = 38

def run(Normalization: protocol_api.ProtocolContext):

######################### Load Labware #####################################
    tiprack_1 = Normalization.load_labware('opentrons_96_tiprack_1000ul', 4, label='1000uL Rack')
    tiprack_2 = Normalization.load_labware('opentrons_96_tiprack_300ul', 5, label='300uL Rack')

    pipette_P1000 = Normalization.load_instrument('p1000_single_gen2', mount = 'right', tip_racks = [tiprack_1])
    pipette_P300 = Normalization.load_instrument('p300_single_gen2', mount = 'left', tip_racks = [tiprack_2])

    enzymes_plate = Normalization.load_labware('nest_96_wellplate_2ml_deep', 2, label = 'Enzymes')
    buffer_reservoir = Normalization.load_labware('nest_1_reservoir_195ml', 6, label = 'Dilution Buffer')


############################# Protocol #####################################

    pipette_P1000.pick_up_tip()
    
    for well_ID, volume_to_add in well_volume_dict_p1000.items():
            
            pipette_P1000.well_bottom_clearance.dispense = pipette_height_dispense
            pipette_P1000.transfer(volume_to_add,buffer_reservoir.wells_by_name()['A1'],enzymes_plate.wells_by_name()[well_ID],
            new_tip = 'never', blow_out = 'true', blowout_location = 'destination well')
    
    pipette_P1000.drop_tip()

    pipette_P300.pick_up_tip()
    
    for well_ID, volume_to_add in well_volume_dict_p300.items():
            
            pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense
            pipette_P300.transfer(volume_to_add,buffer_reservoir.wells_by_name()['A1'],enzymes_plate.wells_by_name()[well_ID],
            new_tip = 'never', blow_out = 'true', blowout_location = 'destination well')

    pipette_P300.drop_tip()
