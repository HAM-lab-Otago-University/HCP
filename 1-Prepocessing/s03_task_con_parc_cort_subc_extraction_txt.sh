#!/bin/bash

### path to files folders
way=/media/DataD800/Alina/main_set

# task folders 
declare -a folders=('3T_tfMRI_EMOTION_analysis_s2' '3T_tfMRI_GAMBLING_analysis_s2' '3T_tfMRI_LANGUAGE_analysis_s2' '3T_tfMRI_MOTOR_analysis_s2' '3T_tfMRI_RELATIONAL_analysis_s2' '3T_tfMRI_SOCIAL_analysis_s2' '3T_tfMRI_WM_analysis_s2')

for folder in ${folders[@]}
do

    ### path to files folders

    path=$way/$folder/analysis

    ### path to subcortical parcellations
    mask_fs_path=/media/DataD800/Alina/atlases/FS_subcort

    ### path to parcellations

    parc=/media/DataD800/Alina/atlases/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii

    ### read the names of subjects
	cd $path/MSMAll_con
    declare -a names
    names=(`ls * | cut -b -6`)


    ### separate subcortical to another folder for both MSMSulc amd MSMAll

    mkdir $path/subcort_MSMAll_con

    for name in ${names[@]} 
    do
        wb_command -cifti-separate \
        $path/MSMAll_con/$name.*.nii  \
        COLUMN  \
        -volume-all \
        $path/subcort_MSMAll_con/$name.MSMAll.con_subc.nii
    done

    ### Apply subc (FS) masks to contrasts for each subj and save txt files to separate folder
	cd $mask_fs_path/
    declare -a mask_names
	mask_names=(` ls *fs-bin.nii.gz | cut -d "." -f 1 `)

    mkdir $path/subc_FS_MSMAll_txts
    for name in ${names[@]}
    do
        mkdir $path/subc_FS_MSMAll_txts/$name
        for mask in ${mask_names[@]}
	    do 
           fslmeants -i $path/subcort_MSMAll_con/$name.*.nii -m $mask_fs_path/$mask.fs-bin.nii.gz -o $path/subc_FS_MSMAll_txts/$name/$name.FS_subcort.$mask.mean.txt
        done
    done

    ### Apply average HCP atlas parcellation to contrasts (MSMAll) and save new parcellated contrasts into new folder and extract txt into another folder

    mkdir  $path/cort_MSMAll_av_Glasser

    mkdir  $path/cort_MSMAll_av_Glasser_txt

    for name in ${names[@]}
    do

        wb_command -cifti-parcellate \
        $path/MSMAll_con/$name.*.dtseries.nii  \
        $parc  \
        COLUMN \
        $path/cort_MSMAll_av_Glasser/$name.MSMAll.aver_parc.ptseries.nii  \
        -method MEAN 

        wb_command -cifti-convert -to-text \
        $path/cort_MSMAll_av_Glasser/$name.MSMAll.aver_parc.ptseries.nii  \
        $path/cort_MSMAll_av_Glasser_txt/$name.MSMAll.aver_parc.txt

    done

done








