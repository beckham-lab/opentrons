#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from opentrons import protocol_api
from opentrons.types import Point # for making point offsets

metadata  = {
    'apiLevel': '2.13',
    'author' : "Mackenzie Denton and Brenna Norton-Baker"}
#updates need testing: changed plate locations & added blow out step (want to add blow out & have it lower in the well)

########### Description ################
# After cleavage by protease, this protocol transfer supernatant containing protein of interest to a new plate, leaving behind spent MagBeads
# Estimated time: 7 min
# Tip usage: 1 rack of p300 tips

############## Variables #############
mag_settle = 0.05 # time in min for mag beads to settle before removing supernatant

supernatant_volume = 255 #uL

pipette_z_offset = 3 #height above the well to remove supernatant and not mag beads
pipette_x_offset = 2.1 #shift in well (right or left) to remove supernatant and not mag beads -- note value is positive

pipette_height_dispense = 15 #height above plate as to not hit mag beads but still be in the well

############################################################################

def run(Transfer_off_MagBeads: protocol_api.ProtocolContext):

######################### Load Labware #####################################
    
    mag_module = Transfer_off_MagBeads.load_module('magnetic module gen2', 1)
    mag_plate = mag_module.load_labware('nest_96_wellplate_2ml_deep', label = 'Enzyme Plate on Mag Mod')
    
    eluted_enzymes = Transfer_off_MagBeads.load_labware('nest_96_wellplate_2ml_deep', 3, label= 'Eluted Enzymes')

    tiprack_1 = Transfer_off_MagBeads.load_labware('opentrons_96_tiprack_300ul', 2, label='300uL Tips')
    pipette_P300 = Transfer_off_MagBeads.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1])

    touch_tip_v_offset = -10
    blow_out_v_offset = -15

############################# Protocol #####################################

    # Pull down mag beads
    mag_module.engage()
    Transfer_off_MagBeads.delay(minutes=mag_settle)

    # Pipette supernantant off
    dictonary = {0:'A1', 1:'A2', 2:'A3', 3:'A4', 4:'A5', 5:'A6', 6:'A7', 7:'A8', 8:'A9', 9:'A10', 10:'A11', 11:'A12'}
    for column_number, column_name in dictonary.items():
            
        pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense

        pipette_P300.pick_up_tip(tiprack_1.wells_by_name()[column_name])

            # mag beads are moved to the corners of the well by the magnets, the corner depends on the well location, beads in odd columns
            # are moved to the right while beads in the even columns are moved to the left

            # since python indexing starts at 0 even columns will have beads to their right and odd columns will have them to their left

            # change the sign of the x offset depending on if the columns are even or odd to pick up supernatant oposite the beads

        if column_number % 2 == 0:
            x = -abs(pipette_x_offset) #if even move to the left 
        else:
            x = abs(pipette_x_offset) #if odd move to the right

        pipette_P300.transfer(supernatant_volume,mag_plate[column_name].bottom().move(Point(x,0,pipette_z_offset)),eluted_enzymes.columns()[column_number],
        blow_out=False, blowout_location='destination well', touch_tip = False, new_tip='never')

        pipette_P300.blow_out(v_offset=blow_out_v_offset)  

        pipette_P300.touch_tip(v_offset=touch_tip_v_offset) 

        pipette_P300.return_tip()
        
    mag_module.disengage()
        



    





