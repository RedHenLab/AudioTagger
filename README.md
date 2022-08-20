# Gsoc2022 - RedHen Labs - Tagging Audio Effects
In GSoc 2022, I will be working with [Redhen Labs](https://www.redhenlab.org/summer-of-code/red-hen-lab-gsoc-2022-projects). 

The objective is to develop a machine learning model to tag sound effects in streams (like police sirens in a news-stream) 
of Red Hen’s data. A single stream of data can contain multiple sound effects, so the model should be able to label them 
from a group of known sound effects like a Multi-label classification problem. YamNet is used a pretrained model in this project.
The video files are converted into audio files. Then they are tagged by YamNet for the sound effects and dumped into 
2 kinds of files:
- SFX Files: These files are based on RedHen's standards where tags are mapped with every frame of audio data. JQ queries can 
be used to filter the SFX tags.
- CSV Files: These files contain tags and their times for the frames. These CSV files are consumed by ELAN tool for annotations
based on the tiers as sound effects.

## Usage
### Singularity Environment
A script called [hpc_script.py](hpc_script.sh) contains all the steps for running in a singularity container.
1. Please clone the repo in RedHen's HPC as a scratch user in the home of the scratch user.
2. Create a folder name with videos required for tagging or use an existing folder from RedHen's mount point.
3. Pass the created folder name as an argument while running the file
 ```hpc_script.sh <<folder_name_with videos>>```
4. After the script is run, an Output folder will be generated with the tagged audio files.

## Future work
- Evaluate other audio taggers and evaluate their results 
- Compare the taggers and use transfer learning to create our own tags
