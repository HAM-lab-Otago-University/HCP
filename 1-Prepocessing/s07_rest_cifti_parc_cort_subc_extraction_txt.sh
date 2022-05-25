#!/bin/bash

# path to files folder 
way=/media/DataD800/Alina/main_set/3T_rfMRI_REST_fix/analysis

#rest types 
declare -a types=('rfMRI_REST1_LR' 'rfMRI_REST1_RL' 'rfMRI_REST2_LR' 'rfMRI_REST2_RL')

for type in ${types[@]}
do

    ### path to files folders

    path=$way/$type

    ### path to subcortical parcellations
    mask_fs_path=/media/DataD800/Alina/atlases/FS_subcort

    ### path to parcellations

    parc=/media/DataD800/Alina/atlases/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii

    ### read the names of subjects
    cd $path
    declare -a names=(`ls * | cut -b -6`)


    ### separate subcortical to another folder for both MSMSulc amd MSMAll

    mkdir $way/$type.subcort_MSMAll

    for name in ${names[@]} 
    do
        wb_command -cifti-separate \
        $path/$name.*.nii  \
        COLUMN  \
        -volume-all \
        $way/$type.subcort_MSMAll/$name.MSMAll.subc.nii
    done

    ### Apply subc (FS) masks to contrasts for each subj and save txt files to separate folder
	cd $mask_fs_path/
    declare -a mask_names
	mask_names=(` ls *fs-bin.nii.gz | cut -d "." -f 1 `)

    mkdir $way/$type.subc_FS_MSMAll_txts
    for name in ${names[@]}
    do
        mkdir $way/$type.subc_FS_MSMAll_txts/$name
        for mask in ${mask_names[@]}
	    do 
           fslmeants -i $way/$type.subcort_MSMAll/$name.*.nii -m $mask_fs_path/$mask.fs-bin.nii.gz -o $way/$type.subc_FS_MSMAll_txts/$name/$name.FS_subcort.$mask.mean.txt
        done
    done

    ### Apply average HCP atlas parcellation to contrasts (MSMAll) and save new parcellated contrasts into new folder and extract txt into another folder

    mkdir  $way/$type.cort_MSMAll_av_Glasser

    mkdir  $way/$type.cort_MSMAll_av_Glasser_txt

    for name in ${names[@]}
    do

        wb_command -cifti-parcellate \
        $path/$name.*.dtseries.nii  \
        $parc  \
        COLUMN \
        $way/$type.cort_MSMAll_av_Glasser/$name.MSMAll.aver_parc.ptseries.nii  \
        -method MEAN 

        wb_command -cifti-convert -to-text \
        $way/$type.cort_MSMAll_av_Glasser/$name.MSMAll.aver_parc.ptseries.nii  \
        $way/$type.cort_MSMAll_av_Glasser_txt/$name.MSMAll.aver_parc.txt

    done

done








