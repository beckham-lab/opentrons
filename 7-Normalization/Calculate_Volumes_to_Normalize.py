import pandas as pd
import numpy as np
import os
from datetime import date

############## Description #################
#This script imports the wells & concentrations from the BCA and outputs a list of wells and volumes
#to normalize the concentrations across the plate. High expressing enzymes are normalized to 0.3 mg/mL
#to not exceed the volume of the well. Medium expressing enzymes are normalized to 0.1 mg/mL. Low/non
#expressing enzymes (below 0.1mg/mL) are unchanged. 

#It also autogenerates the OT2 protocol for normalization. 

#### Calculation of Normalization Volumes ####

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'Normalization_input.xlsx')
sheet_name_conc = 'Sheet1'
sheet_name_wells = 'Sheet2'
columns_to_use =  ['1','2', '3', '4', '5', '6', '7', '8','9','10','11','12']

low_cut_off_conc = 0.099 #below this considered low or no yield
med_cut_off_conc = 0.734 #above this and the volume to normalize to 0.1 mg/mL exceeds well limit

concentration_target = 0.1 #mg/mL
concentration_target_high_expressing = 0.3 #mg/mL

volume_in_well = 245 #uL

#import Excel sheet with 96-well plate map of concentrations, convert to list with Well IDs
df_concentrations = pd.read_excel(file_path, sheet_name_conc, usecols = columns_to_use, nrows=8, skiprows=1)
df_wells = pd.read_excel(file_path, sheet_name_wells, usecols = ['Well'], nrows=96)
df_concentrations_list = pd.DataFrame({'Concentration':df_concentrations.values.ravel()})
df_list = pd.concat([df_wells, df_concentrations_list], axis=1)

#define the targent concentration for each well, then calculate the volume to add to reach that concentration
target_concentration = np.where(df_list['Concentration'] < low_cut_off_conc, df_list['Concentration'], 
                        np.where(df_list['Concentration'] > med_cut_off_conc, concentration_target_high_expressing, concentration_target))
df_list['Target Concentration'] = target_concentration
df_list['Final Volume'] = (df_list['Concentration'].mul(volume_in_well)).div(df_list['Target Concentration'])
df_list['Volume to Add'] = (df_list['Final Volume']).sub(volume_in_well).round(decimals=1)

#this corrects for low volume additions so only two pipettes (p1000 and p300) are needed (less than 20 uL)
volume_to_add_corrected = np.where(df_list['Volume to Add'] > 20, df_list['Volume to Add'], 0) 
df_list['Volume to Add'] = volume_to_add_corrected
file_path2 = os.path.join(script_dir, 'Normalization_calcs.xlsx')
df_list.to_excel(file_path2, index=False)

#cut the list down to just well and volume to add
df_list_for_robot = df_list[['Well', 'Volume to Add']]

#exports an excel file with the final concentrations, if needed
df_final_concentrations = df_list[['Well', 'Concentration', 'Target Concentration']]
df_final_concentrations = df_final_concentrations.rename(columns={'Target Concentration':'Final Concentration'})
# file_path4 = os.path.join(script_dir, 'Final_concentrations.xlsx')
# df_final_concentrations.to_excel(file_path4, index=False)

# Remove rows where 'volume to add' column is 0
df_split = df_list_for_robot[df_list_for_robot['Volume to Add'] != 0]

#split the list - one for p1000 and other for p300
df_p1000 = df_split[df_split['Volume to Add'] > 300]
df_p300 = df_split[df_split['Volume to Add'] <= 300]

well_volume_dict_p1000 = dict(zip(df_p1000['Well'], df_p1000['Volume to Add']))
well_volume_dict_p300 = dict(zip(df_p300['Well'], df_p300['Volume to Add']))

print(well_volume_dict_p1000)
print(well_volume_dict_p300)

###### Generate Script for OT2 #############

# Define the file name for the new script
today = date.today()
date_str = today.strftime("%Y-%m-%d")
print(date_str)
new_script_file = f'{date_str}_Normalization_OT2.py'

#script contents
section1 = '''
from opentrons import protocol_api

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

############# Description ###############
# This protocol normalizes the enzyme concentrations.  
# Estimated time: 15-20 min
# Tip usage: 1 p1000 tip, 1 p300 tip
'''
section2 ='''
######################## Volumes for Normalizations ########################
'''
section3 = '''
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
'''
# Open the new script file for writing
output_path = os.path.join(script_dir, new_script_file)

with open(output_path, 'w') as f:
    # Write the script content to the file
    f.write(section1)
    f.write(section2)
    f.write('well_volume_dict_p1000 = {}\n'.format(well_volume_dict_p1000))
    f.write('well_volume_dict_p300 = {}\n\n'.format(well_volume_dict_p300))
    f.write(section3)
