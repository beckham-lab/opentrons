import pandas as pd
import os 
from datetime import date

#modify path
custom_labware_file_path = '/Users/bnortonb/Documents/Automation_paper/opentrons/Custom_labware/thomsoninstrument_24_wellplate_10400ul.json'

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path_wells = os.path.join(script_dir,'input_inoculation_cherrypicking.xlsx')
file_path_sourceplate1 = os.path.join(script_dir,'sourceplate1.xlsx')
file_path_sourceplate2 = os.path.join(script_dir,'sourceplate2.xlsx')
file_path_sourceplate3 = os.path.join(script_dir,'sourceplate3.xlsx')
file_path_sourceplate4 = os.path.join(script_dir,'sourceplate4.xlsx')
file_path_sourceplate5 = os.path.join(script_dir,'sourceplate5.xlsx')
file_path_newplatemap= os.path.join(script_dir,'output_new_platemap.xlsx')

directory = os.path.abspath(os.path.join(os.path.abspath(os.path.join(script_dir, os.pardir)), os.pardir))
df_wells = pd.read_excel(file_path_wells)

# group by source plate and create dictionary of dictionaries
plate_dict = {}
for plate, data in df_wells.groupby('Source Plate'):
    well_dict = {}
    for index, row in data.iterrows():
        # Check if Source Well is not nan before adding to the dictionary
        if pd.notna(row['Source Well']):
            if row['Source Well'] in well_dict:
                well_dict[row['Source Well']].append(row['Destination Well'])
            else:
                well_dict[row['Source Well']] = [row['Destination Well']]
    plate_dict[plate] = well_dict

#map to 4 24 well plates
plate_mapping = {}
rows_96 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
rows_24 = ['A', 'B', 'C', 'D']

# For plates A and B, based on 1-6 and 7-12 columns of the 96-well plate
for i, plate_label in enumerate(['cell_culture_plateA', 'cell_culture_plateB']):
    for j, row_96 in enumerate(rows_96[:4]):  # Only the first 4 rows
        for col in range(1, 7):  # Columns 1-6
            key = f"{row_96}{col + i * 6}"  # Adjusts based on plate A or B
            val = (plate_label, f"{rows_24[j]}{col}")
            plate_mapping[key] = val

# For plates C and D, based on 1-6 and 7-12 columns of the 96-well plate
for i, plate_label in enumerate(['cell_culture_plateC', 'cell_culture_plateD']):
    for j, row_96 in enumerate(rows_96[4:]):  # Last 4 rows
        for col in range(1, 7):  # Columns 1-6
            key = f"{row_96}{col + i * 6}"  # Adjusts based on plate C or D
            val = (plate_label, f"{rows_24[j]}{col}")
            plate_mapping[key] = val

# Create a nested dictionary of transfers for source to destination plates
transfers = {}
for src_plate in plate_dict.keys():
    transfers[src_plate] = {
        'cell_culture_plateA': [],
        'cell_culture_plateB': [],
        'cell_culture_plateC': [],
        'cell_culture_plateD': []
    }

transfer_commands = []

for src_plate, well_dict in plate_dict.items():
    for src_well, dest_wells in well_dict.items():
        for dest_well in dest_wells:
            real_plate, real_dest = plate_mapping[dest_well]
            cmd = f"    pipette_300.transfer(inoculation_volume, {src_plate}.wells_by_name()['{src_well}'], {real_plate}.wells_by_name()['{real_dest}'], blow_out=True, blowout_location='destination well', touch_tip=False, new_tip='always', mix_before=(2, 100))"
            transfer_commands.append(cmd)

destination_order = ['cell_culture_plateA', 'cell_culture_plateB', 'cell_culture_plateC', 'cell_culture_plateD']
rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
columns = [str(i) for i in range(1, 13)]  # Assuming 12 columns

# Create a lookup dictionary to map destination wells to their source wells
lookup_dict = {}
for src_plate in transfers.keys():
    for dest_plate in transfers[src_plate].keys():
        for src_well, dest_well in transfers[src_plate][dest_plate]:
            lookup_dict[(dest_plate, dest_well)] = (src_plate, src_well)

for dest_plate in destination_order:
    for row in rows:
        for col in columns:
            dest_well = row + col
            if (dest_plate, dest_well) in lookup_dict:
                src_plate, src_well = lookup_dict[(dest_plate, dest_well)]
                cmd = f"    pipette_300.transfer(inoculation_volume, {src_plate}.wells_by_name()['{src_well}'], {dest_plate}.wells_by_name()['{dest_well}'], blow_out=True, blowout_location='destination well', touch_tip = False, new_tip='always', mix_before=(2, 100))"
                transfer_commands.append(cmd)

transfer_section = "\n".join(transfer_commands)

# Make a new plate map with Sample IDs
df_sourceplate1 = pd.read_excel(file_path_sourceplate1)

# Create dictionaries for easier lookup of Sample ID
sourceplate1_dict = dict(zip(df_sourceplate1['Well'], df_sourceplate1['Sample ID']))

# Check if sourceplate2.xlsx exists before reading it
if os.path.exists(file_path_sourceplate2):
    df_sourceplate2 = pd.read_excel(file_path_sourceplate2)
    sourceplate2_dict = dict(zip(df_sourceplate2['Well'], df_sourceplate2['Sample ID']))
else:
    sourceplate2_dict = {}

# Check if sourceplate3.xlsx exists before reading it
if os.path.exists(file_path_sourceplate3):
    df_sourceplate3 = pd.read_excel(file_path_sourceplate3)
    sourceplate3_dict = dict(zip(df_sourceplate3['Well'], df_sourceplate3['Sample ID']))
else:
    sourceplate3_dict = {}

# Check if sourceplate3.xlsx exists before reading it
if os.path.exists(file_path_sourceplate4):
    df_sourceplate4 = pd.read_excel(file_path_sourceplate4)
    sourceplate4_dict = dict(zip(df_sourceplate4['Well'], df_sourceplate4['Sample ID']))
else:
    sourceplate4_dict = {}

    # Check if sourceplate3.xlsx exists before reading it
if os.path.exists(file_path_sourceplate5):
    df_sourceplate5 = pd.read_excel(file_path_sourceplate5)
    sourceplate5_dict = dict(zip(df_sourceplate5['Well'], df_sourceplate5['Sample ID']))
else:
    sourceplate5_dict = {}

# For each row in the input_inoculation_cherrypicking Excel file, find the Sample ID
sample_ids = []
for _, row in df_wells.iterrows():
    plate = row['Source Plate']
    well = row['Source Well']
    
    if plate == 'sourceplate1':
        sample_ids.append(sourceplate1_dict.get(well, 'N/A'))
    elif plate == 'sourceplate2':
        sample_ids.append(sourceplate2_dict.get(well, 'N/A'))
    elif plate == 'sourceplate3':
        sample_ids.append(sourceplate3_dict.get(well, 'N/A'))
    elif plate == 'sourceplate4':
        sample_ids.append(sourceplate4_dict.get(well, 'N/A'))
    elif plate == 'sourceplate5':
        sample_ids.append(sourceplate5_dict.get(well, 'N/A'))
    else:
        sample_ids.append('N/A')

df_wells['Sample ID'] = sample_ids

# Save the updated df_wells dataframe to a new Excel file
df_wells.to_excel(file_path_newplatemap, sheet_name='New_platemap', index=False)

###### Generate Script for OT2 #############

# Define the file name for the new script
today = date.today()
date_str = today.strftime("%Y-%m-%d")
new_script_file = f'{date_str}_inoculation_cherrypicking_OT2.py'

#script contents
section1 = '''
from opentrons import protocol_api
from opentrons.types import Point # for making point offsets
import json
import os

metadata  = {
    'apiLevel': '2.13',
    'author' : "Brenna Norton-Baker"}

########### Description ################
# After transformation, this protocol inoculates 4 24-well plates containing media from 1 96-well plate containing transformed cells.
# Estimated time: 1 h
# Tip usage: 1 rack of p300 tips
'''
section2 = '''
############## Variables #############
inoculation_volume = 20 #uL

p300_well_bottom_clearance_aspirate = 2
p300_well_bottom_clearance_dispense = 2

############# Protocol ###############
def run(protocol: protocol_api.ProtocolContext):

    tiprack_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2, label='200uL Filter Rack')
    pipette_300 = protocol.load_instrument('p300_single_gen2', mount = 'left', tip_racks=[tiprack_1])
    

    # Check if running in simulation mode
    if os.environ.get('RUNNING_ON_PI') != 'true':
        # Use the relative file path
        with open('{custom_labware_file_path}') as labware_file:
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

    sourceplate1 = protocol.load_labware('nest_96_wellplate_2ml_deep', 1, label = 'Source Plate 1')
    sourceplate2 = protocol.load_labware('nest_96_wellplate_2ml_deep', 4, label = 'Source Plate 2')
    sourceplate3 = protocol.load_labware('nest_96_wellplate_2ml_deep', 7, label = 'Source Plate 3')
    sourceplate4 = protocol.load_labware('nest_96_wellplate_2ml_deep', 10, label = 'Source Plate 4')
    sourceplate5 = protocol.load_labware('nest_96_wellplate_2ml_deep', 11, label = 'Source Plate 5')

       
    pipette_300.well_bottom_clearance.aspirate = p300_well_bottom_clearance_aspirate
    pipette_300.well_bottom_clearance.dispense = p300_well_bottom_clearance_dispense
'''
section3 = transfer_section

# Open the new script file for writing
output_path = os.path.join(script_dir, new_script_file)

with open(output_path, 'w') as f:
    # Write the script content to the file
    f.write(section1)
    f.write(section2.format(custom_labware_file_path=custom_labware_file_path))  
    f.write(section3)
