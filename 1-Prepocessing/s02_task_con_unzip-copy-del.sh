#!/bin/bash

### path to files folders

path=/media/DataD800/Alina/main_set

### folders of tasks

declare -a folders=('3T_tfMRI_EMOTION_analysis_s2' '3T_tfMRI_GAMBLING_analysis_s2' '3T_tfMRI_LANGUAGE_analysis_s2' '3T_tfMRI_MOTOR_analysis_s2' '3T_tfMRI_RELATIONAL_analysis_s2' '3T_tfMRI_SOCIAL_analysis_s2' '3T_tfMRI_WM_analysis_s2')

### the number of contrast in specific task

declare -a numcon=(3 6 4 21 4 6 11)

###

i=0
while [ $i -le 6 ];
do
    ### switch to task folder   
    cd $path/${folders[i]}
    mkdir $path/${folders[i]}/folders
    mkdir $path/${folders[i]}/analysis
    mkdir $path/${folders[i]}/analysis/MSMAll_con
    
	### read names of subjects in task folder
	cd $path/${folders[i]}/archives/
    declare -a subjects=(`ls *.zip | cut -b  -6`)
    
	### parse through subjects
    for subject in ${subjects[@]}
    do
        #unzip
        unzip -q -o $path/${folders[i]}/archives/$subject*.zip -d $path/${folders[i]}/folders/
        #copy
        cp $path/${folders[i]}/folders/$subject/MNINonLinear/Results/*/*_level2_MSMAll.feat/GrayordinatesStats/cope${numcon[i]}.feat/cope1.dtseries.nii $path/${folders[i]}/analysis/MSMAll_con/$subject.${folders[i]}.cope${numcon[i]}.dtseries.nii
        #del
        rm -r $path/${folders[i]}/folders/$subject
    done
    
    ((i+=1))
done

