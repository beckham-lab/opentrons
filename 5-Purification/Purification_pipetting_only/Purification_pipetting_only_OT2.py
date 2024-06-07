from opentrons import protocol_api
from opentrons.types import Point # for making point offsets

metadata  = {
    'apiLevel': '2.13',
    'author' : "Mackenzie Denton and Brenna Norton-Baker"}
########### Description ################
# After transfer to the 96-well plate, this protocol will perform the additional washes and add the protease to cleave the proteins of interest from the MagBeads
# Estimated time: X min (3 min per column)
# Tip usage: 2 racks of p300 tips (1 for washes + 1 for protease addition)

############ Variables #################

mag_settle = 0.11 # time in min for mag beads to settle before removing supernatant

supernatant_volume = 300 #uL
protease_volume = 30 #uL

pipette_z_offset = 3 #height above the well to remove supernatant and not mag beads
pipette_x_offset = 2.1 #shift in well (right or left) to remove supernatant and not mag beads -- note value is positive

pipette_height_dispense_waste = 30 #height above trash reservoir so tips dont touch waste
pipette_height_dispense_wash = 3 #dispense into liquid, to mix
pipette_height_dispense_SUMO = 3 #dispense into liquid, use new tips each time

pipette_mix_speed = 200 #uL/s

time_for_mixing_with_protease = 4 #hours
mixing_interval = 10 #min

############################################################################

def run(Purification: protocol_api.ProtocolContext):

######################### Load Labware #####################################

    mag_module = Purification.load_module('magnetic module gen2', 1)
    mag_plate = mag_module.load_labware('nest_96_wellplate_2ml_deep', label = 'Enzyme Plate on Mag Mod')
    
    wash_buffer = Purification.load_labware('nest_96_wellplate_2ml_deep', 2, label = 'Wash Buffer')
    cleavage_buffer = Purification.load_labware('nest_96_wellplate_2ml_deep', 3, label = 'Cleavage Buffer')
    protease_plate = Purification.load_labware('nest_96_wellplate_2ml_deep', 8, label = 'Protease Plate')
    waste = Purification.load_labware('nest_96_wellplate_2ml_deep', 9, label= 'Waste')

    tiprack_1 = Purification.load_labware('opentrons_96_tiprack_300ul', 4, label='300uL Tips for Purification')
    tiprack_2 = Purification.load_labware('opentrons_96_tiprack_300ul', 7, label='300uL Tips for protease addition')
    pipette_P300 = Purification.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_1,tiprack_2])

    pipette_P300.flow_rate.aspirate = pipette_mix_speed
    pipette_P300.flow_rate.dispense = pipette_mix_speed

############################# Protocol #####################################
    
    # Pull down mag beads

    dictonary = {0: 'A1', 1:'A2', 2:'A3', 3:'A4', 4:'A5', 5:'A6', 6:'A7', 7:'A8', 8:'A9', 9:'A10', 10:'A11', 11:'A12'}
    for column_number, column_name in dictonary.items():

        pipette_P300.pick_up_tip(tiprack_1.wells_by_name()[column_name])

        locations = [wash_buffer, wash_buffer, wash_buffer, cleavage_buffer, cleavage_buffer, cleavage_buffer]
        for location in locations:

            mag_module.engage()
            Purification.delay(minutes=mag_settle)

            # mag beads are moved to the corners of the well by the magnets, the corner depends on the well location, beads in odd columns
            # are moved to the right while beads in the even columns are moved to the left
            # since python indexing starts at 0 even columns will have beads to their right and odd columns will have them to their left
            # change the sign of the x offset depending on if the columns are even or odd to pick up supernatant oposite the beads

            if column_number % 2 == 0:
                x = -abs(pipette_x_offset) #if even move to the left 
            else:
                x = abs(pipette_x_offset) #if odd move to the right

            pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_waste
            pipette_P300.transfer(supernatant_volume,mag_plate[column_name].bottom().move(Point(x,0,pipette_z_offset)),waste.columns()[column_number],
            blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='never')
            pipette_P300.touch_tip()

            mag_module.disengage()

            pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_wash
            pipette_P300.transfer(supernatant_volume,location.columns(column_number), mag_plate.columns()[column_number],  
            blow_out=False, touch_tip = False, new_tip='never', mix_after=(3,200))

        pipette_P300.blow_out()
        pipette_P300.return_tip()
        
    mag_module.disengage()
    Purification.pause('Add SUMO Protease to SUMO plate')
    
    ##### Protease Addition #####
    for column_number, column_name in dictonary.items():
        pipette_P300.pick_up_tip(tiprack_2.wells_by_name()[column_name])
        pipette_P300.well_bottom_clearance.dispense = pipette_height_dispense_SUMO
        pipette_P300.transfer(protease_volume,protease_plate.columns(0),mag_plate.columns(column_number), new_tip='never', blow_out=True, blowout_location='destination well', mix_after=(2,200))
        pipette_P300.blow_out()
        pipette_P300.touch_tip()
        pipette_P300.return_tip()

    Purification.pause('Comtinue for pipette mixing or cancel run to seal plate and move to plate shaker.')

    #### Mixing for protease cleavage #####

    # Calculate the total number of intervals for 4 hours
    total_repetitions = int((time_for_mixing_with_protease * 60) / mixing_interval)

    # Perform mixing for the calculated number of intervals
    for _ in range(total_repetitions):
        Purification.delay(minutes=mixing_interval)
        for column_number, column_name in dictonary.items():
            pipette_P300.pick_up_tip(tiprack_2.wells_by_name()[column_name])
            pipette_P300.mix(3, 150, mag_plate[column_name])
            pipette_P300.blow_out()
            pipette_P300.touch_tip()
            pipette_P300.return_tip()
        
    


