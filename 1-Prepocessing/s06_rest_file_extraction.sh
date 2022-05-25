#!/bin/bash

### path to files folders

path=/media/DataD800/Alina/main_set/3T_rfMRI_REST_fix

###create analysis folder

declare -a types=('rfMRI_REST1_LR' 'rfMRI_REST1_RL' 'rfMRI_REST2_LR' 'rfMRI_REST2_RL')

mkdir $path/folders/
mkdir $path/analysis/

for type in ${types[@]}
do
    mkdir $path/analysis/$type
done

### read names of subj = names of folders
cd $path/archives
declare -a subjects=(`ls *.zip | cut -b 1-6`)

###sorting specific contrast to folders
for subject in ${subjects[@]}
do

unzip -q -o $path/archives/$subject*.zip -d $path/folders/

    for type in ${types[@]}
    do
        cp $path/folders/$subject/MNINonLinear/Results/$type/*MSMAll_hp2000_clean* $path/analysis/$type/$subject.$type.Atlas_MSMAll_hp2000_clean.dtseries.nii
    done

rm -r $path/folders/$subject

done
