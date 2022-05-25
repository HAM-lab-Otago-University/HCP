#!/bin/bash

### path to files folders

path1=/media/DataD800/Alina/main_set/3T_Structural_preproc
path2=/media/DataD800/Alina/main_set/3T_Structural_preproc_extended

#create additional folders 
mkdir $path1/folders
mkdir $path2/folders
mkdir $path2/folders/dirs

# read subj names
cd $path2/archives
declare -a subjects=(`ls *.zip | cut -b 1-6`)

for subject in ${subjects[@]}
do

    #unzip
    unzip -q -o $path1/archives/$subject*.zip -d $path1/folders/
    unzip -q -o $path2/archives/$subject*.zip -d $path2/folders/dirs/

    #copy
    cp -R $path2/folders/dirs/$subject/T1w/$subject  $path2/folders/
    cp -R $path1/folders/$subject/T1w/$subject/stats  $path2/folders/$subject/

    #del
    rm -r $path1/folders/$subject

done

rm -r $path2/folders/dirs


#activate Freesurfer and set subj folder

export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh

export SUBJECTS_DIR=$path2/folders


#extract and sace aparc and aseg stats table

asegstats2table --subjects ${subjects[@]} --meas volume --delimiter comma -t $path2/aseg_stats.txt

aparcstats2table --hemi lh --subjects ${subjects[@]} --parc aparc.a2009s  --meas thickness --delimiter comma -t $path2/aparc_stats_thickness_a2009s_lh.txt
aparcstats2table --hemi lh --subjects ${subjects[@]} --parc aparc.a2009s  --meas area --delimiter comma -t $path2/aparc_stats_area_a2009s_lh.txt

aparcstats2table --hemi rh --subjects ${subjects[@]} --parc aparc.a2009s  --meas thickness --delimiter comma -t $path2/aparc_stats_thickness_a2009s_rh.txt
aparcstats2table --hemi rh --subjects ${subjects[@]} --parc aparc.a2009s  --meas area --delimiter comma -t $path2/aparc_stats_area_a2009s_rh.txt





