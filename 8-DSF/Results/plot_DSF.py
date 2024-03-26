from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import os

#imports the Melt Curve Derivative & Amplification Results excel files (in format of export from Bio-Rad software)
#it doesn't like the original results file - I found that just resaving as an .xlsx file works (even though it says it already is that)
#make sure to examine the plots and reset the threshold for the derivative if needed
#the import cuts out the last five rows (0.2 degrees C) of derivative data, bc values can get kind of weird at the end and mess up the threshold

### Variables ###
threshold_deriv = -6
skip_footer_length = 5 #these are the rows left out of the derivative curve import

### Define File Paths ###
script_dir = os.path.dirname(os.path.abspath(__file__))

plots_deriv_dir = 'plots_deriv'
plots_amp_dir = 'plots_amp'

folder_path_output_deriv = os.path.join(script_dir, plots_deriv_dir)
folder_path_output_amp = os.path.join(script_dir, plots_amp_dir)


# Create directories if they don't exist
if not os.path.exists(folder_path_output_deriv):
    os.makedirs(folder_path_output_deriv)
if not os.path.exists(folder_path_output_amp):
    os.makedirs(folder_path_output_amp)

# File paths and variables
script_dir = os.path.dirname(os.path.abspath(__file__))

#search for the derivative results file
derivative_file = [file for file in os.listdir(script_dir) if 'Derivative Results.xlsx' in file]
if derivative_file:
    file_path_deriv = os.path.join(script_dir, derivative_file[0])
else:
    raise FileNotFoundError("Derivative results file not found. Try resaving it as .xlsx")
sheet_name_deriv = 'SYBR'

#search for the amplifcation results file
amplification_file = [file for file in os.listdir(script_dir) if 'Amplification Results.xlsx' in file]
if amplification_file:
    file_path_amp = os.path.join(script_dir, amplification_file[0])
else:
    raise FileNotFoundError("Amplification results file not found. Try resaving it as .xlsx")
sheet_name_amp = 'SYBR'

#output paths
folder_path_output_deriv = os.path.join(script_dir, 'plots_deriv')
folder_path_output_amp = os.path.join(script_dir, 'plots_amp')

#sample ID path
file_path_well_identities = os.path.join(script_dir, 'Sample_IDs.xlsx')
sheet_name_well_identities = 'Sheet1'

file_path_export = os.path.join(script_dir, 'Tm_values.xlsx')

### Plotting ###

#plots the derivaties results
df_deriv = pd.read_excel(file_path_deriv, sheet_name_deriv, usecols=None, skipfooter=skip_footer_length)
#drop the first empty column
df_deriv = df_deriv.drop(df_deriv.columns[0], axis=1)
df_no_temp = df_deriv.drop(df_deriv.columns[0], axis=1)
list_columns = df_no_temp.columns.tolist()

for col in list_columns:
    fig, ax = plt.subplots()
    ax.plot(df_deriv['Temperature'], df_deriv[col])
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('RFU')
    plt.title(col)
    plt.xlim(25,100)
    plt.ylim(-140, 40)
    fig.savefig(f"{folder_path_output_deriv}/{col}.png")
    plt.close(fig)

#plots the amplification results
df_amp = pd.read_excel(file_path_amp, sheet_name_amp, usecols=None)
#drop the first empty column
df_amp = df_amp.drop(df_amp.columns[0], axis=1)
df_no_temp = df_amp.drop(df_amp.columns[0], axis=1)
list_columns = df_no_temp.columns.tolist()

for col in list_columns:
    fig, ax = plt.subplots()
    ax.plot(df_amp['Temperature'], df_amp[col])
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('RFU')
    plt.title(col)
    plt.xlim(25,100)
    plt.ylim(2000, 5000)
    fig.savefig(f"{folder_path_output_amp}/{col}.png")
    plt.close(fig)

#removes data columns (wells) that don't meet the derivative threshold (no Tm determined)
columns_below_threshold = df_deriv.columns[(df_deriv < threshold_deriv).any()].tolist()
number_of_columns = len(columns_below_threshold)

df_columns_below_threshold = df_deriv[columns_below_threshold]

df_columns_below_threshold = df_columns_below_threshold.assign(new_column=df_deriv['Temperature'].values)
df_columns_below_threshold = df_columns_below_threshold.reindex(columns=['new_column'] + list(df_columns_below_threshold.columns[:-1]))
df_columns_below_threshold = df_columns_below_threshold.rename(columns={'new_column': 'Temperature'})

well_names = list(df_columns_below_threshold.columns[1:])

#finds the local minima
local_minima_indices = []

for col in df_columns_below_threshold.columns[1:]:
    column_data = df_columns_below_threshold[col].values
    local_minima, _ = find_peaks((-1*column_data), distance=20, prominence = 12)
    local_minima_indices.append(local_minima)

minima_df = pd.DataFrame({'Well': df_columns_below_threshold.columns[1:], 'Local Minima': local_minima_indices})

#append the values to a new dataframe
temperature_values = []
for well, minima in zip(well_names, local_minima_indices):
    temperature_values.append([df_columns_below_threshold['Temperature'][i] for i in minima])

minima_temperature_dict = {}
for well, minima_temperature in zip(well_names, temperature_values):
    minima_temperature_dict[well] = minima_temperature

minima_temperature_df = pd.DataFrame.from_dict(minima_temperature_dict, orient='index')

print(minima_temperature_df)

#exports the Tms to an excel sheet
df_Tm_values = pd.DataFrame({'Well': df_columns_below_threshold.columns[1:]})

# Get the number of columns in minima_temperature_df
num_columns = len(minima_temperature_df.columns)

# Loop through the columns to add
for i in range(3):
    if i < num_columns:
        df_Tm_values[f'IP_{i + 1}'] = minima_temperature_df[i].tolist()
    else:
        df_Tm_values[f'IP_{i + 1}'] = np.nan

#import well identities
df_well_identities = pd.read_excel(file_path_well_identities, sheet_name_well_identities,  usecols=None)

# Create df for appended data
appended_df = pd.concat([df_well_identities.set_index('Well'), df_Tm_values.set_index('Well')], axis=1, join='outer')

# Export the DataFrame with sample IDs
appended_df.to_excel(file_path_export, index=True)

print(appended_df)
