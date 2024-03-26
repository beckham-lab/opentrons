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
# After lysis supernatant is removed, this protocol transfers the MagBeads from 4 24-well plates to 1 96-well plate.
# Estimated time: 
# Tip usage: 1 rack of p300 tips

############## Variables #############
transfer_volume = 600 #uL, split into two transfers

p300_well_bottom_clearance_aspirate = 0.3
p300_well_bottom_clearance_dispense = 15

pipette_y_offset = -9 #applied to quadrant C and D to move to B1-B6 (for C) and B7-B12 (for D)

aspiration_speed_mixing  = 300
aspiration_speed = 75
dispense_speed = 100

############## Protocol #############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 7, label='HALF LOADED - 300uL Rack')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 4, label='HALF LOADED - 300uL Rack')
    pipette_multi_P300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1, tiprack_2])   

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

    enzymes_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 10, label = 'Enzymes Plate')
   
    pipette_multi_P300.well_bottom_clearance.aspirate = p300_well_bottom_clearance_aspirate

############## Protocol #############
    
    source_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

    destination_wells_A = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    destination_wells_B = ['A7', 'A8', 'A9', 'A10', 'A11', 'A12']
    destination_wells_C = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6'] #with offset
    destination_wells_D = ['A7', 'A8', 'A9', 'A10', 'A11', 'A12'] #with offset

    pipette_multi_P300.flow_rate.dispense = dispense_speed

    # #Plate A and B without offset
    destination_wells_list_of_list1 = [destination_wells_A,destination_wells_B]
    culture_plate_list1 = [cell_culture_plateA, cell_culture_plateB]

    for plate, destination_wells_list in zip(culture_plate_list1, destination_wells_list_of_list1):
        for source_well, destination_well in zip(source_wells, destination_wells_list):
            destination_well = enzymes_plate.wells_by_name()[destination_well].bottom().move(Point(0, 0, p300_well_bottom_clearance_dispense))

            pipette_multi_P300.pick_up_tip()
            pipette_multi_P300.move_to(plate.wells_by_name()[source_well].bottom().move(Point(0, 0, p300_well_bottom_clearance_aspirate)))
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed_mixing
            pipette_multi_P300.mix(repetitions=2, volume=100)
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed
            pipette_multi_P300.aspirate(transfer_volume/2, plate.wells_by_name()[source_well])
            pipette_multi_P300.dispense(transfer_volume/2, destination_well)
            pipette_multi_P300.blow_out()
            pipette_multi_P300.move_to(plate.wells_by_name()[source_well].bottom().move(Point(0, 0, p300_well_bottom_clearance_aspirate)))
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed_mixing
            pipette_multi_P300.mix(repetitions=2, volume=100)
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed
            pipette_multi_P300.aspirate(transfer_volume/2, plate.wells_by_name()[source_well])
            pipette_multi_P300.dispense(transfer_volume/2, destination_well)
            pipette_multi_P300.blow_out()
            pipette_multi_P300.return_tip()

    #Plate C and D with offset
    destination_wells_list_of_list2 = [destination_wells_C,destination_wells_D]
    culture_plate_list2 = [cell_culture_plateC, cell_culture_plateD]

    for plate, destination_wells_list in zip(culture_plate_list2, destination_wells_list_of_list2):
        for source_well, destination_well in zip(source_wells, destination_wells_list):
            destination_well = enzymes_plate.wells_by_name()[destination_well].bottom().move(Point(0, pipette_y_offset, p300_well_bottom_clearance_dispense))

            pipette_multi_P300.pick_up_tip()
            pipette_multi_P300.move_to(plate.wells_by_name()[source_well].bottom().move(Point(0, 0, p300_well_bottom_clearance_aspirate)))
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed_mixing
            pipette_multi_P300.mix(repetitions=2, volume=100)
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed
            pipette_multi_P300.aspirate(transfer_volume/2, plate.wells_by_name()[source_well])
            pipette_multi_P300.dispense(transfer_volume/2, destination_well)
            pipette_multi_P300.blow_out()
            pipette_multi_P300.move_to(plate.wells_by_name()[source_well].bottom().move(Point(0, 0, p300_well_bottom_clearance_aspirate)))
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed_mixing
            pipette_multi_P300.mix(repetitions=2, volume=100)
            pipette_multi_P300.flow_rate.aspirate = aspiration_speed
            pipette_multi_P300.aspirate(transfer_volume/2, plate.wells_by_name()[source_well])
            pipette_multi_P300.dispense(transfer_volume/2, destination_well)
            pipette_multi_P300.blow_out()
            pipette_multi_P300.return_tip()
