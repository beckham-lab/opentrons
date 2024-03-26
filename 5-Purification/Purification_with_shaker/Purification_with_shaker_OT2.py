from opentrons import protocol_api
from opentrons.types import Point # for making point offsets

metadata  = {
    'apiLevel': '2.13',
    'author' : "Mackenzie Denton and Brenna Norton-Baker"}
#needs testing - reordered to remove 1st & last shake & SUMO shake 

########### Description ################
# After transfer to the 96-well plate, this protocol will perform the additional washes and add the protease to cleave the proteins of interest from the MagBeads
# Estimated time: 1 h
# Tip usage: 2 racks of p300 tips (1 for washes, tips are returned, + 1 for protease addition, tips to waste)

############ Variables #################
supernatant_volume = 225 #uL
protease_volume = 30 #uL

shake_time_wash = 3 #min
mag_settle = 0.05 # time in min for mag beads to settle before removing supernatant
shake_speed = 1200 #rpm

pipette_z_offset = 3 #height above the well to remove supernatant and not mag beads
pipette_x_offset = 2.1 #shift in well (right or left) to remove supernatant and not mag beads -- note value is positive
pipette_height_dispense_waste = 30 #height above trash reservoir so tips dont touch waste
pipette_height_dispense_wash = 15 #height above plate as to not hit mag beads but still be in the well
pipette_height_dispense_SUMO = 3 #dispense into liquid, use new tips each time

############################################################################

def run(Purification: protocol_api.ProtocolContext):

######################### Load Labware #####################################

    shaker = Purification.load_module('heaterShakerModuleV1', 7)
    shaker_plate = shaker.load_labware('opentrons_96_deep_well_adapter_nest_wellplate_2ml_deep', label = 'Enzyme Plate on Shaker')
    
    mag_module = Purification.load_module('magnetic module gen2', 1)
    mag_plate = mag_module.load_labware('nest_96_wellplate_2ml_deep', label = 'Enzyme Plate on Mag Mod')
    
    wash_buffer = Purification.load_labware('nest_96_wellplate_2ml_deep', 2, label = 'Wash Buffer')
    cleavage_buffer = Purification.load_labware('nest_96_wellplate_2ml_deep', 3, label = 'Cleavage Buffer')
    sumo_protease = Purification.load_labware('nest_96_wellplate_2ml_deep', 6, label = 'SUMO Protease')
    Waste = Purification.load_labware('nest_96_wellplate_2ml_deep', 9, label= 'Waste')

    tiprack_1 = Purification.load_labware('opentrons_96_tiprack_300ul', 5, label='300uL Tips')
    tiprack_2 = Purification.load_labware('opentrons_96_tiprack_300ul', 11, label='300uL Tips')
    pipette_P300 = Purification.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1,tiprack_2])

############################# Protocol #####################################

    locations = [wash_buffer,wash_buffer,cleavage_buffer,cleavage_buffer]
    for index, location in enumerate(locations):

        # Move plate to mag mod
        Purification.pause('Move plate to Mag Mod')
        
        # Pull down mag beads
        mag_module.engage()
        Purification.delay(minutes=mag_settle)

        # Pipette supernantant off
        dictonary = {0:'A1', 1:'A2', 2:'A3', 3:'A4', 4:'A5', 5:'A6', 6:'A7', 7:'A8', 8:'A9', 9:'A10', 10:'A11', 11:'A12'}
        for column_number, column_name in dictonary.items():
            
            pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_waste

            pipette_P300.pick_up_tip(tiprack_1.wells_by_name()[column_name])

            # mag beads are moved to the corners of the well by the magnets, the corner depends on the well location, beads in odd columns
            # are moved to the right while beads in the even columns are moved to the left

            # since python indexing starts at 0 even columns will have beads to their right and odd columns will have them to their left

            # change the sign of the x offset depending on if the columns are even or odd to pick up supernatant opposite the beads

            if column_number % 2 == 0:
                x = -abs(pipette_x_offset) #if even move to the left 
            else:
                x = abs(pipette_x_offset) #if odd move to the right

            pipette_P300.transfer(supernatant_volume,mag_plate[column_name].bottom().move(Point(x,0,pipette_z_offset)),Waste.columns()[column_number],
            blow_out=True, blowout_location='destination well', touch_tip = True, new_tip='never')

            pipette_P300.touch_tip() #Do this a second time to remove drops

            pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_wash

            pipette_P300.transfer(supernatant_volume,location.columns(column_number), mag_plate.columns()[column_number],  
            blow_out=True, blowout_location='destination well', touch_tip = True, new_tip='never')

            pipette_P300.touch_tip() #Do this a second time to remove drops

            pipette_P300.return_tip()
        
        # Move plate back to shaker
        mag_module.disengage()
        shaker.open_labware_latch()
        Purification.pause('Move plate to shaker')
        shaker.close_labware_latch()

        # Check if this is not the last iteration, if so, then shake
        if index != len(locations) - 1:  
            # Shake for X min
            shaker.set_and_wait_for_shake_speed(shake_speed)
            Purification.delay(minutes=shake_time_wash)
            shaker.deactivate_shaker()
            shaker.open_labware_latch()

    Purification.pause('Add SUMO Protease to SUMO plate')

    #Protease addition
    pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_SUMO
    pipette_P300.transfer(protease_volume,sumo_protease.columns(0),[shaker_plate.columns()[column_number] for column_number in range(12)], new_tip='always', blow_out=True, blowout_location='destination well')
    shaker.open_labware_latch()



    





