#!/bin/bash

#set path to download folder where all archives are stored
path=/media/DataD800/Alina/main_set

#names of folders will be created and name of file modalities
declare -a types=('3T_rfMRI_REST1_preproc' '3T_rfMRI_REST2_preproc' '3T_rfMRI_REST_fix' '3T_Structural_preproc_extended' '3T_Structural_preproc' '3T_tfMRI_EMOTION_analysis_s2' '3T_tfMRI_EMOTION_preproc' '3T_tfMRI_GAMBLING_analysis_s2' '3T_tfMRI_GAMBLING_preproc' '3T_tfMRI_LANGUAGE_analysis_s2' '3T_tfMRI_LANGUAGE_preproc' '3T_tfMRI_MOTOR_analysis_s2' '3T_tfMRI_MOTOR_preproc' '3T_tfMRI_RELATIONAL_analysis_s2' '3T_tfMRI_RELATIONAL_preproc' '3T_tfMRI_SOCIAL_analysis_s2' '3T_tfMRI_SOCIAL_preproc' '3T_tfMRI_WM_analysis_s2' '3T_tfMRI_WM_preproc')

#list through modality
for type in ${types[@]}
do

#create folder first
mkdir $path/$type
mkdir $path/$type/archives
#then move files with specific modality to the folder
for file in $path/*$type* ; do mv $file $path/$type/archives/ ; done

done
