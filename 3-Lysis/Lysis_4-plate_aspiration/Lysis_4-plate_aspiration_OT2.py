from opentrons import protocol_api
import json
from opentrons.types import Point # for making point offsets
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/Protocol_code/Custom_labware/thomsoninstrument_24_wellplate_10400ul_on_homebuilt_magmod.json'

########### Description ################
# After lysis & MagBead binding, this protocol removes the supernatant from a four 24-well plates on homebuilt magmods and leaves behind the MagBeads.
# Then 300 uL of Wash Buffer is added as the first wash in the purification. 
# Estimated time: 25 min
# Tip usage: 2 racks and 1 addtional column of 3rd rack, 300 uL tips

########### Variables ################

volume_lysis_buffer_remove = 1800/2 #uL, half because two tips per well
pipette_x_offset = 6 #to pull from off center of the MagBeads
pipette_y_offset = 5.5 #to align two tips per well
z_offset = 2 

volume_wash1 = 150 #uL, half because two tips per well
                            
pipette_height_aspirate_lysis = 0
pipette_height_dispense = 20 # to keep tip clean between buffers
pipette_height_aspirate_reservoirs = 3 #mm, prevents it from hitting the bottom

########### Protocol ################
def run(protocol: protocol_api.ProtocolContext):

    ######################### Load Labware #####################################
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1, label='300uL Rack')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 2, label='300uL Rack')
    tiprack_3 = protocol.load_labware('opentrons_96_tiprack_300ul', 3, label='300uL Rack')

    pipette_multi_P300 = protocol.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1, tiprack_2, tiprack_3])   

    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open(custom_labware_file_path ) as labware_file:
            labware_def = json.load(labware_file)
            cell_culture_plateA = protocol.load_labware_from_definition(labware_def, 8, label = 'Cell Culture Plate A')
            cell_culture_plateB = protocol.load_labware_from_definition(labware_def, 9, label = 'Cell Culture Plate B')
            cell_culture_plateC = protocol.load_labware_from_definition(labware_def, 5, label = 'Cell Culture Plate C')
            cell_culture_plateD = protocol.load_labware_from_definition(labware_def, 6, label = 'Cell Culture Plate D')
    else:
        # Use the absolute file path
        cell_culture_plateA = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul_on_homebuilt_magmod', 8, label = 'Cell Culture Plate A') 
        cell_culture_plateB = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul_on_homebuilt_magmod', 9, label = 'Cell Culture Plate B') 
        cell_culture_plateC = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul_on_homebuilt_magmod', 5, label = 'Cell Culture Plate C') 
        cell_culture_plateD = protocol.load_labware('thomsoninstrument_24_wellplate_10400ul_on_homebuilt_magmod', 6, label = 'Cell Culture Plate D')

    waste = protocol.load_labware('agilent_1_reservoir_290ml', 7, label = 'Waste') 
    wash_buffer = protocol.load_labware('nest_1_reservoir_195ml', 4, label = 'Wash Buffer') 

    pipette_multi_P300.well_bottom_clearance.dispense = pipette_height_dispense

    pipette_multi_P300.pick_up_tip()

    cell_culture_plates = [cell_culture_plateA,cell_culture_plateB, cell_culture_plateC, cell_culture_plateD ]
    
    for culture_plate in cell_culture_plates:
        for column_number in range(1, 7):  # Loop through all wells of each plate
            column_name = 'A' + str(column_number)

            pipette_multi_P300.well_bottom_clearance.aspirate = pipette_height_aspirate_lysis

            if column_number % 2 == 0:
                x = abs(pipette_x_offset)  # if even move to the left
            else:
                x = -abs(pipette_x_offset)  # if odd move to the right

            pipette_multi_P300.transfer(volume_lysis_buffer_remove,
                                         culture_plate[column_name].bottom().move(Point(x, 0, 0)),
                                         waste.wells_by_name()['A1'],
                                         blow_out=True, blowout_location='destination well', touch_tip=False,
                                         new_tip='never')

            pipette_multi_P300.return_tip()
            pipette_multi_P300.pick_up_tip()
            pipette_multi_P300.well_bottom_clearance.aspirate = pipette_height_aspirate_reservoirs
            pipette_multi_P300.transfer(volume_wash1, wash_buffer.wells_by_name()['A1'],
                                        culture_plate.wells_by_name()[column_name],
                                        blow_out=True, blowout_location='destination well', touch_tip=False,
                                        new_tip='never')

    pipette_multi_P300.return_tip()





        