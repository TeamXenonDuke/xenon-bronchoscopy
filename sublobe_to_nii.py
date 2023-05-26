# Function sublobe_to_nii
# Imports sublobe mask, does some reorienting, and outputs as a nii
# Note CT nifti must already be present

def sublobe_to_nii(sublobe_path, data_path):

    import nibabel as nb
    import numpy as np
    import pdb as pdb

    # Get sublobe nifti (current stupidly pulled out of ITK-Snap)
    sublobe = nb.load(sublobe_path)

    # Get header from ct, pull this from process routine eventually
    ct_nii = nb.load(data_path + 'ct.nii')

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

    
    nb.save(ct_whole_mask_nii, (data_path + 'ct_whole_lung_mask.nii'))

    return()