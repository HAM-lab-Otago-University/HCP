# Capturing Brain-Cognition Relationship: Integrating Task-BasedfMRI Across Tasks Markedly Boosts Prediction and Reliability and Reveals the Role of Frontoparietal Areas  

https://www.biorxiv.org/content/10.1101/2021.10.31.466638v2.full 

Abstract 

Capturing individual differences in cognition is central to human neuroscience. Yet our ability to estimate cognitive abilities via brain MRI is still poor in both prediction and reliability. Our study tested if this inability was partly due to the over-reliance on 1) non-task MRI modalities and 2) single, rather than multiple, modalities. We directly compared predictive models comprising different sets of MRI modalities (e.g., task vs. non-task). Using the Human Connectome Project (n=873, 473 females, after quality control), we integrated task-based functional MRI (tfMRI) across seven tasks along with other non-task MRI modalities (structural MRI, resting-state functional connectivity). We applied two approaches to integrate multimodal MRI, stacked vs. flat models, and implemented16 combinations of machine-learning algorithms. The model integrating all modalities via stacking Elastic Net provided unprecedented prediction (r=.57) and excellent test-retest reliability (ICC>.75) in capturing general cognitive abilities. Importantly, compared to the model integrating across non-task modalities (r=.27), the model integrating tfMRI across tasks led to significantly higher prediction (r=.56) while still providing excellent test-retest reliability (ICC>.75). The model integrating tfMRI across tasks was driven by areas in the frontoparietal network and by tasks that are cognition-related (working-memory, relational processing, and language). This result is consistent with the parieto-frontal integration theory of intelligence. Accordingly, our results sharply contradict the recently popular notion that tfMRI is not appropriate for capturing individual differences in cognition. Instead, our study suggests that tfMRI, when used appropriately (i.e., by drawing information across the whole brain and across tasks and by integrating with other modalities), provides predictive and reliable sources of information for individual differences in cognitive abilities, more so than non-task modalities. 

 
----- 

For reproducibility purposes, we provided all scripts we used in this study as well as supplementary files here.  

For those who would like to apply our final models to their data, we provided coefficients of each brain modalities here:  
HCP/images/   - cortex CIFTI files and 
HCP/tables/  -  tables with top20 and all parcels 

 
Note users will need to edit these scripts, so that the designated folders and files match with their local settings.  
 
Prerequisite software for our script: 
wb_command (HCP Workbench Command) (v1.5.0, https://www.humanconnectome.org/software/connectome-workbench) 
FSL (6.0.5, https://fsl.fmrib.ox.ac.uk/fsl/fslwiki) 
FreeSurfer (freesurfer-linux-centos7_x86_64-7.1.0-20200511-813297b, https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) 

 
We also borrowed several files from other different projects: 

HCP/images/meta-analysis_contrast_file_gii/       
Here we converted the Activation Likelihood Estimate (ALE) map of significant foci that showed associations with various cognitive abilities( Santarnecchi et al. 2017, downloaded from http://www.tmslab.org/netconlab-fluid.php), to a CIFTI format.  

HCP-MMP1_UniqueRegionList.csv and MMP_in_MNI_corr.nii.gz    
These are HCP-MMP1 atlases file taken from  https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/atlases.html  

MNI152_T1_1mm_brain.nii.gz    
This is a template taken from the standard FSL template libraries. 

Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii   
This a Glasser’s atlas file originally published at https://balsa.wustl.edu/file/3VLx  

destrieux2009_rois_labels_lateralized.csv and destrieux2009_rois_lateralized.nii.gz    
These are Destrieux 2009 atlas files taken from Nilearn  https://github.com/nilearn/nilearn/blob/1607b524/nilearn/datasets/atlas.py#L185  https://www.nitrc.org/frs/download.php/11942/  

 
For those who would like to apply our final models to their data, we provided coefficients of each brain modalities here:  
HCP/images/   - cortex CIFTI files and 

HCP/tables/  -  tables with top20 and all parcels 

 



