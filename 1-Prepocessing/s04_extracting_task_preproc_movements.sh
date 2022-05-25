#!/bin/bash

### path to files folders
way=/media/DataD800/Alina/main_set

declare -a folders=('3T_tfMRI_EMOTION_preproc' '3T_tfMRI_GAMBLING_preproc' '3T_tfMRI_LANGUAGE_preproc' '3T_tfMRI_MOTOR_preproc' '3T_tfMRI_RELATIONAL_preproc' '3T_tfMRI_SOCIAL_preproc' '3T_tfMRI_WM_preproc')

for folder in ${folders[@]}
do

    ### path to files folders

    path_in=$way/$folder
    mkdir $path_in/folders
    mkdir $path_in/analysis
    mkdir $path_in/analysis/confounds
    path_out=$path_in/analysis/confounds

    ### read the names of subjects
    cd $path_in/archives/
    declare -a names=(`ls *.zip | cut -b 1-6`)
    # echo ${names[@]}



    ### main loop
    for subject in ${names[@]} 
    do

        #make dir
        mkdir $path_out/$subject
        mkdir $path_out/$subject/LR
        mkdir $path_out/$subject/RL

        #unzip
        unzip -q -o $path_in/archives/$subject*.zip -d $path_in/folders/

        #copy
        cp $path_in/folders/$subject/*/*/*_LR/Movement_*.txt $path_out/$subject/LR/

        cp $path_in/folders/$subject/*/*/*_RL/Movement_*.txt $path_out/$subject/RL/

        #del
        rm -r $path_in/folders/$subject 


    done

done





