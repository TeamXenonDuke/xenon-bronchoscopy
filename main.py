### Main function for turning CT, XeMRI, and sublobe mask into a report

import os
import nibabel as nb
import pdb
import numpy as np
import dicom_process_ct as dicom_process_ct
import mat_vent_to_nii
import mat_gx_to_nii
import sublobe_to_nii
import ants_reg
import generate_report

from scipy.io import loadmat
from tkinter import filedialog
from tkinter import *
from mat_vent_to_nii import mat_vent_to_nii
from mat_gx_to_nii import mat_gx_to_nii
from sublobe_to_nii import sublobe_to_nii
from dicom_process_ct import dicom_process_ct
from ants_reg import ants_reg
from generate_report import generate_report

# Set Flags
process_ct = 1 #1 = process CT, 0 = don't process CT
run_reg = 3 #1 = rigid, 2 = syn, 3 = apply registrations only (i.e. reg already performed) 
subject_id = 'OS-017'
scan_id = 's1' #s1 or s2 etc.
flavor = 'vent' # 'vent' or 'gx' 

# Set paths
orig_data_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/OS_017_sample_data_tryout/orig_data/'
processing_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/OS_017_sample_data_tryout/processing_data/'

if flavor == 'vent':
    mat_path = orig_data_path + '/' + subject_id + '_' + scan_id + '_rad_' + flavor + '.mat' 
if flavor == 'gx':
    mat_path = orig_data_path + '/' + subject_id + '_' + scan_id + flavor + '.mat'



# Don't touch anything past this. note -- you can leave the sublobe exported from ITK-Snap as a zipped nifti, you don't need to unzip it first.  
ct_path = orig_data_path + '/ct/'
sublobe_path = orig_data_path + '/ZUNU_vida-sublobes.nii.gz'
#ct_whole_path = processing_path + '/ct_whole_lung_mask.nii'
#ct_nii_path = processing_path + '/ct.nii'
ct_whole_path = orig_data_path + '/ct_whole_lung_mask.nii'
ct_nii_path = orig_data_path + '/ct.nii'


### Process CT and Sublobe 

# Turn CT into a nifti
if process_ct == 1:
    ct_nifti = dicom_process_ct(ct_path, ct_nii_path)

# Turn Sublobe mask into a nifti
sublobe_to_nii(sublobe_path, orig_data_path)


# Process Dedicated Vent 
if flavor == 'vent':
    vent_mask_path = processing_path + '/dedvent_mask.nii'    
    vent_bin_path = processing_path + '/dedvent_bin.nii'
    mat_vent_to_nii(mat_path, processing_path)
    
# Process GX
if flavor == 'gx':
    vent_mask_path = processing_path + '/gx_vent_mask.nii'
    vent_bin_path = processing_path + '/gx_vent_bin.nii'
    vent_norm_path = processing_path + '/gx_vent_norm.nii'
    bar_bin_path = processing_path + '/bar_bin.nii'
    rbc_bin_path = processing_path + '/rbc_bin.nii'

    mat_gx_to_nii(mat_path, processing_path)

# Return to run ANTs call with whatever vent mask was specified    
ants_reg(run_reg, vent_mask_path, ct_whole_path, orig_data_path, processing_path)

# Generate the Vent report
if flavor == 'vent':
    generate_report(processing_path, subject_id, scan_id, 'vent', vent_mask_path, vent_bin_path)

if flavor == 'gx':
    generate_report(processing_path, subject_id, scan_id,'gx_vent', vent_mask_path, vent_bin_path)
    generate_report(processing_path, subject_id, scan_id, 'bar', vent_mask_path, bar_bin_path)
    generate_report(processing_path, subject_id, scan_id, 'rbc', vent_mask_path, rbc_bin_path)
    




