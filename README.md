# Introduction

This repository contains scripts to perform automated steps in the recombinant expression and purification of proteins in *E. coli* assisted by the OT-2 robot. Futher details on the development and use of these protocols can be found in the paper cited below. 

## Comments

- In order to use the simulate function to test protocols, the user must define the path to the custom labware in each protocol script. 
    - Swap out custom_labware_file_path = 'path/to/your/custom_labware/ for your path to the custom labware files

- Some protocols display a 'Protocol analysis failure' warning when imported into Opentrons software due to defining the custom labware file path for simulation. Ignore the error and proceed to set up the run. 

- Many of the available protocols return the tips to their rack to facilitate washing and reuse. 



## Citation
Norton-Baker, B., Denton, M.C.R., Murphy, N.P., Fram, B., Lim, S., Erickson, E., Gauthier, N.P., & Beckham, G.T. Enabling high-throughput enzyme discovery and engineering with a low-cost, robot-assisted pipeline.  *In review*