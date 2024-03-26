from opentrons import protocol_api

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}
#updates need testing: changed all blow_out = 'true' to True. 

############# Description ###############
# After cleavage, this protocol sets up the BCA concentration assay.  
# Estimated time: 6 min per plate, 12 min total
# Tip usage: 1 rack + 4 columns of p20 tips, 2 columns of p300 tips

################ Prep ###################
 #prepare 29 mL of BCA regaent (29 mL Reagent A and 0.58 mL of Reagent B)
 #load BCA regent into A1 (11 mL, for samples col 1-6), A2 (11 mL, for samples col. 7-12), A3 (7 ml, for controls) of 12 well NEST reservoir
 
 #amounts are in a Excel File saved to the Teams account: prepare controls plate of BSA: A1(2000ug/mL); B1(1500ug/mL); C1(1000ug/mL); D1(750ug/mL)
 #E1(500ug/mL); F1(250ug/mL); G1(125ug/mL); H1(25ug/mL); A2(12.5ug/mL); B2(0ug/mL)
 #Use your specific buffer to prepare controls
 
############### Varaibles #################
p300_multi_well_bottom_clearance_dispense = 10
p20_multi_well_bottom_clearance_dispense = 0
p20_multi_well_bottom_clearance_aspirate= 4 

############### Protocol #################

def run(BCA_assay: protocol_api.ProtocolContext):

############# Load Labware ################

    enzyme_plate = BCA_assay.load_labware('nest_96_wellplate_2ml_deep', 1,label='enzyme plate')
    assay_plate1 = BCA_assay.load_labware('corning_96_wellplate_360ul_flat',6, label='assay plate 1, col. 1-6')
    assay_plate2 = BCA_assay.load_labware('corning_96_wellplate_360ul_flat',3, label='assay plate 1, col. 7-12')
    BSA_plate = BCA_assay.load_labware('nest_96_wellplate_2ml_deep',2, label='BSA_controls')
    BCA_reagent_reservoir = BCA_assay.load_labware('nest_12_reservoir_15ml',8, label='BCA reagent')

    tiprack_1 = BCA_assay.load_labware('opentrons_96_tiprack_20ul', 4, label='20uL Rack 1')
    tiprack_2 = BCA_assay.load_labware('opentrons_96_tiprack_20ul', 5, label='20uL Rack 2')
    tiprack_3 = BCA_assay.load_labware('opentrons_96_tiprack_300ul', 7, label='300uL Rack 1')

    pipette_multi_20 = BCA_assay.load_instrument('p20_multi_gen2', mount = 'right', tip_racks=[tiprack_1, tiprack_2])
    pipette_multi_300 = BCA_assay.load_instrument('p300_multi_gen2', mount = 'left', tip_racks=[tiprack_3])

    pipette_multi_300.well_bottom_clearance.dispense = p300_multi_well_bottom_clearance_dispense 
    pipette_multi_20.well_bottom_clearance.dispense = p20_multi_well_bottom_clearance_dispense
    pipette_multi_20.well_bottom_clearance.aspirate = p20_multi_well_bottom_clearance_aspirate

########################################
    
    list_assay_plate1 = [0,1,2,3,4,5]
    list_BSA_plate = [0,1]
    list_assay_plate2 = [6,7,8,9,10,11]
    list_distribute_assayplate1_samples = [0,1,2,3,4,5]
    list_distribute_assayplate1_controls = [6,7]
    list_distribute_assayplate2_samples = [6,7,8,9,10,11]
    list_distribute_assayplate2_controls = [4,5]

#add enzyme to assay plate 1
    for column in list_assay_plate1:
        pipette_multi_20.transfer(10,enzyme_plate.columns()[column], assay_plate1.columns()[column],
        new_tip = 'always', blow_out = True, blowout_location = 'destination well')

#add controls to assay plate 1
    for column in list_BSA_plate:
        pipette_multi_20.transfer(10,BSA_plate.columns()[column], assay_plate1.columns()[column + 6],
        new_tip = 'always', blow_out = True, blowout_location = 'destination well')

#add BCA reagent to assay plate 1
    pipette_multi_300.pick_up_tip()
    for column in list_distribute_assayplate1_samples:
        pipette_multi_300.transfer(200,BCA_reagent_reservoir.wells_by_name()['A1'], assay_plate1.columns()[column],
        new_tip = 'never', blow_out = True, blowout_location = 'destination well')
    for column in list_distribute_assayplate1_controls:
        pipette_multi_300.transfer(200,BCA_reagent_reservoir.wells_by_name()['A3'], assay_plate1.columns()[column],
        new_tip = 'never', blow_out = True, blowout_location = 'destination well')
    pipette_multi_300.drop_tip()

#add enzyme to assay plate 2
    for column in list_assay_plate2:
        pipette_multi_20.transfer(10,enzyme_plate.columns()[column], assay_plate2.columns()[column],
        new_tip = 'always', blow_out = True, blowout_location = 'destination well')

#add controls to assay plate 2
    for column in list_BSA_plate:
        pipette_multi_20.transfer(10,BSA_plate.columns()[column], assay_plate2.columns()[column + 4],
        new_tip = 'always', blow_out = True, blowout_location = 'destination well')

#add BCA reagent to assay plate 2
    pipette_multi_300.pick_up_tip()
    for column in list_distribute_assayplate2_samples:
        pipette_multi_300.transfer(200,BCA_reagent_reservoir.wells_by_name()['A2'], assay_plate2.columns()[column],
        new_tip = 'never', blow_out = True, blowout_location = 'destination well')
    for column in list_distribute_assayplate2_controls:
        pipette_multi_300.transfer(200,BCA_reagent_reservoir.wells_by_name()['A3'], assay_plate2.columns()[column],
        new_tip = 'never', blow_out = True, blowout_location = 'destination well')
    pipette_multi_300.drop_tip()


    
        