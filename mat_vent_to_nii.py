# FUNCTION mat_vent_to_nii
# Provide a mat file path and a string, and return the mask and normalized vent

def mat_vent_to_nii(mat_path, data_path):

    import numpy as np
    import nibabel as nb
    import pdb
    from scipy.io import loadmat

    matfile = loadmat(mat_path)

    #EVERYTHING Dedicated VENT 
    vent_path = data_path + 'dedvent_norm.nii'
    vent = np.absolute(matfile['dedi_vent_highreso'])
    vent_norm = (vent - np.amin(vent))/np.amax(vent)

    #Put it in the correct orientation
    vent_norm_transpose = np.transpose(vent_norm, (1, 0, 2))

    # Make it into a nifti object
    vent_nii = nb.Nifti1Image(vent_norm_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    vent_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])

    vent_nii.header.set_qform(None, code = 2)

    # Save it as a file
    nb.save(vent_nii, vent_path)


    # Ventilation binning
    vent_bin_path = data_path + 'dedvent_bin.nii'
    vent_bin = np.absolute(matfile['dedi_vent_highreso_binning'])

    # Put it in the correct orientation
    vent_bin_transpose = np.transpose(vent_bin, (1, 0, 2))

    # Make it into a nifti object
    vent_bin_nii = nb.Nifti1Image(vent_bin_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    vent_bin_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    vent_bin_nii.header.set_qform(None, code =2)

    # Save it as a file
    nb.save(vent_bin_nii, vent_bin_path)


    # Ventilation mask
    vent_mask_path = data_path + 'dedvent_mask.nii'

    vent_mask = vent_bin - 1
    vent_mask[vent_mask > 1] = 1

    # Put it in the correct orientation
    vent_mask_transpose = np.transpose(vent_mask, (1, 0, 2))

    # Make it into a nifti object
    vent_mask_nii = nb.Nifti1Image(vent_mask_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    vent_mask_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    vent_mask_nii.header.set_qform(None, code =2)

    ## Save it as a file
    nb.save(vent_mask_nii, vent_mask_path)

    return()
