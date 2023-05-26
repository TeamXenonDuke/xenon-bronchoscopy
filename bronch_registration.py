# Bronch report code
#
# Begun by David Mummy 5/18/21
#
#
# Overall description:
# Takes CT mask and deformably registers it to lung boundary mask.
# For each bronchopulmonary segment, add up the bins to get segmental metrics.

# YOU WILL NEED TO SET THIS TO USE EITHER THE GX VENT OR DEDICATED VENT, DEPENDING ON WHETHER YOU ARE
# USING VENTILATION OR BAR/RBC MEASUREMENTS FOR THE ANALYSIS

# import the necessary libraries
import os
import nibabel as nb
import pdb
import numpy as np
import matplotlib.pyplot as pyplot
from scipy.io import loadmat

# Home-brewed "dicom_process" function that turns CT DICOMs into .nii files
from dicom_process_ct import dicom_process_ct # CT DICOMs

# Turn a GX Mat file into Nifties. May not need to do this with new GX outputs? For now, need to 
from mat_to_nii import mat_to_nii



########### 1. DEFINE PATHS, SET THRESHOLDS ############

# General data path & MAT-file name. Need a forward slash at the end
data_path = '/Users/mummy/Desktop/temp/'
matfile_path = 'LH-016_gx.mat'

## THIS NEEDS TO POINT TO A VENT MASK WHETHER IT'S DED VENT OR GX VENT MASK
vent_mask_path = data_path + 'ded_vent_mask.nii'


# Turn CT DICOMs into Nifti? 1 = yes, 0 = no (if already done)
process_ct = 0

# Turn MAT file into Nifti? 1 = yes, 0 = no (if already done)
process_mat = 1

# Select registration: 1 = rigid (if there are issues) or 2 = deformable
run_registration = 0


## Nothing from here on should need to be edited for regular use ###

# Define path to CT DICOMs, and desired output path to xenon nifti's

ct_path = data_path + 'ct/dicoms'
ct_nii_path = data_path + 'ct_nii.nii'
output_file_name = data_path + 'sublobe_whole_reg.nii'

sublobe_whole_path = data_path + 'whole_lung_mask.nii'

# Load CT from DICOMs.
if process_ct == 1:
    ct_nii = dicom_process_ct(ct_path, ct_nii_path)

# Load MAT file
if process_mat ==1 :
    matfile = mat_to_nii(matfile_path, data_path)

pdb.set_trace()

# Get sublobe nifti (current stupidly pulled out of ITK-Snap)
sublobe = nb.load(data_path + 'ZUNU_vida-sublobes.nii')

# Get header from ct, pull this from process routine eventually
ct_nii = nb.load(data_path + 'ct_nii.nii')

# Get CT metadata
meta = ct_nii.header

# Get image from sublobe mask
sublobe_img = sublobe.get_fdata()

# Flip it to coronal view
sublobe_img_transpose = np.transpose(sublobe_img, (0,2,1))

# Turn it into a Nifti, using the metadata from the CT header
nii_sublobe_transpose = nb.Nifti1Image(sublobe_img_transpose, np.eye(4), meta)

# And save it
nb.save(nii_sublobe_transpose, (data_path + 'sublobe_transpose.nii'))

# Now do the same thing, but for a CT whole lung mask
ct_whole_mask_img = sublobe_img_transpose


ct_whole_mask_img[ct_whole_mask_img >= 1] = 1

ct_whole_mask_nii = nb.Nifti1Image(ct_whole_mask_img, np.eye(4), meta)

nb.save(ct_whole_mask_nii, (data_path + 'whole_lung_mask.nii'))


############# 3. RUN 3D REGISTRATION ####################

# The run_registration parameter to determine registration type is set at the beginning by the user

if run_registration == 1:

    cmd_rigid = ('./antsRegistration -d 3 -verbose 1 '
        '-o [rigid_deform_matrix, '+output_file_name+'] -n BSpline '
        '-r ['+vent_mask_path+', '+sublobe_whole_path+',2] '
        '-t Rigid[0.15] '
        '-m MI['+vent_mask_path+', '+sublobe_whole_path+', 1, 32, Regular, 1] '
        '-c [100x40x20, 1e-6, 10] -f 4x2x1 -s 0x0x0 '
        )

    os.system(cmd_rigid)
    print('Rigid registration complete')

elif run_registration == 2:
    cmd_syn_withmask = ('./antsRegistration -d 3 -verbose 1 '
        '-o [syn_deform_matrix, '+output_file_name+'] -n BSpline '
        '-r ['+vent_mask_path+', '+sublobe_whole_path+',2] '
        '-t Rigid[0.15] '
        '-m MI['+vent_mask_path+', '+sublobe_whole_path+', 1, 32, Regular, 1] '
        '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 '
        '-t Affine[0.15] '
        '-m MI['+vent_mask_path+', '+sublobe_whole_path+', 1, 32, Regular, 1] '
        '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 '
        '-t Syn[0.1, 3.0, 0.5] '
        '-m MI['+vent_mask_path+', '+sublobe_whole_path+', 1, 32, Regular, 1] '
        '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 ')

    os.system(cmd_syn_withmask)
    print('CT-Gas Registration Completed')


# Apply transform to sublobe mask
## SWITCH BACK REFERENCES TO VEN MASK HERE 
cmd_apply = ('./antsApplyTransforms -d 3 '
        '-i ' +data_path+ 'sublobe_transpose.nii '
        '-o ' +data_path+ 'sublobe_transpose_reg.nii '
        '-n multilabel '
        '-r '+data_path+'ded_vent_mask.nii '
        '-t [syn_deform_matrix0GenericAffine.mat, 0] '
        '-t syn_deform_matrix1Warp.nii.gz ')

os.system(cmd_apply)

# And to CT

cmd_apply_ct = ('./antsApplyTransforms -d 3 '
        '-i ' +data_path+ 'ct_nii.nii '
        '-o ' +data_path+ 'ct_reg.nii '
        '-n linear '
        '-r '+data_path+'ded_vent_mask.nii '
        '-t [syn_deform_matrix0GenericAffine.mat, 0] '
        '-t syn_deform_matrix1Warp.nii.gz ')

os.system(cmd_apply_ct)

