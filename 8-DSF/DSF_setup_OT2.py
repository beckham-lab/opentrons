from opentrons import protocol_api

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}
#updates to check: added touch tip for sypro transfer - tends to drop drops as it moves

############# Description ###############
# After normalization, this protocol sets up a plate for Sypro-dye based DSF.
# Estimated time: 7 min
# Tip usage: 1 column of p20 tips, 1 rack of p300 tips
    
####################### Define Varaibles #################################

volume_enzyme_transfer = 45 #uL, recommended 0.1-0.5 mg/mL
volume_sypro_transfer = 5 #uL, concentration 50X (final concentration 5X), prepare 900 uL total (add 9 uL from stock to 891 uL H2O)
list_all_columns_sampled = [0,1,2,3,4,5,6,7,8,9,10,11]

############################################################################

def run(DSF_setup: protocol_api.ProtocolContext):

######################### Load Labware #####################################

    enzyme_plate = DSF_setup.load_labware('nest_96_wellplate_2ml_deep', 2, label = 'Enzyme Plate')
    sypro_plate = DSF_setup.load_labware('nest_96_wellplate_2ml_deep', 5, label= 'Sypro') #load 100 uL per well in column 1
    pcr_plate = DSF_setup.load_labware('biorad_96_wellplate_200ul_pcr', 3, label = 'PCR Plate')

    tiprack_1 = DSF_setup.load_labware('opentrons_96_tiprack_20ul', 9, label='20uL Tips')
    tiprack_2 = DSF_setup.load_labware('opentrons_96_tiprack_300ul', 8, label='300uL Tips')
    pipette_multi_20 = DSF_setup.load_instrument('p20_multi_gen2', mount = 'right', tip_racks = [tiprack_1])
    pipette_multi_300 = DSF_setup.load_instrument('p300_multi_gen2', mount = 'left', tip_racks = [tiprack_2])
############################ Protocol #####################################

# distribute sypro dye to PCR plate  
    pipette_multi_20.pick_up_tip()
    pipette_multi_20.distribute(volume_sypro_transfer,sypro_plate.columns()[0], [pcr_plate.columns()[column] for column in list_all_columns_sampled],
    new_tip = 'never', blow_out = True, blowout_location = 'source well')
    pipette_multi_20.touch_tip()
    pipette_multi_20.drop_tip()

#transfer enzymes to PCR plate  
    for column in list_all_columns_sampled:

        pipette_multi_300.transfer(volume_enzyme_transfer, enzyme_plate.columns()[column], pcr_plate.columns()[column],
        new_tip = 'always', blow_out = True, blowout_location = 'destination well')

