# FUNCTION mat_gx_to_nii
# Provide a mat file path and a string, and return the normalized UTE, mask, normalized vent, and non-normalized membrane and RBC

def mat_gx_to_nii(mat_path, data_path):

    import numpy as np
    import nibabel as nb
    import pdb
    from scipy.io import loadmat

     
    matfile = loadmat(mat_path)

    # EVERYTHING GX GAS
    gx_vent_path = data_path + 'gx_vent_norm.nii'
    gx_vent = np.absolute(matfile['image_gas_highreso']) #pre-refactor name: 'gx_vent_highreso'
    gx_vent_norm = (gx_vent - np.amin(gx_vent))/np.amax(gx_vent)

    # Put it in the correct orientation
    gx_vent_norm_transpose = np.transpose(gx_vent_norm, (1, 0, 2))

    # Make it into a nifti object
    gx_vent_nii = nb.Nifti1Image(gx_vent_norm_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    gx_vent_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])

    gx_vent_nii.header.set_qform(None, code = 2)

    # Save it as a file
    nb.save(gx_vent_nii, gx_vent_path)


    # Ventilation binning
    gx_vent_bin_path = data_path + 'gx_vent_bin.nii'
    gx_vent_bin = np.absolute(matfile['image_gas_binned']) # pre-refactor name: 'gx_vent_highreso_binning'

    # Put it in the correct orientation
    gx_vent_bin_transpose = np.transpose(gx_vent_bin, (1, 0, 2))

    # Make it into a nifti object
    gx_vent_bin_nii = nb.Nifti1Image(gx_vent_bin_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    gx_vent_bin_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    
    gx_vent_bin_nii.header.set_qform(None, code =2)

    # Save it as a file
    nb.save(gx_vent_bin_nii, gx_vent_bin_path)


    # GX Ventilation mask
    gx_vent_mask_path = data_path + 'gx_vent_mask.nii'

    gx_vent_mask = gx_vent_bin - 1
    gx_vent_mask[gx_vent_mask > 1] = 1

    # Put it in the correct orientation
    gx_vent_mask_transpose = np.transpose(gx_vent_mask, (1, 0, 2))

    # Make it into a nifti object
    gx_vent_mask_nii = nb.Nifti1Image(gx_vent_mask_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    gx_vent_mask_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    
    gx_vent_mask_nii.header.set_qform(None, code =2)

    # Save it as a file
    nb.save(gx_vent_mask_nii, gx_vent_mask_path)


    # EVERYTHING MEMBRANE
    # Data

    membrane_path = data_path + 'mem.nii'
    membrane = np.absolute(matfile['image_membrane2gas']) #pre-refactor name: 'bar2gas'

    # Put it in the correct orientation
    membrane_transpose = np.transpose(membrane, (1, 0, 2))

    # Make it into a nifti object
    membrane_nii = nb.Nifti1Image(membrane_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    membrane_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    
    membrane_nii.header.set_qform(None, code =2)

    # Save it as a file
    nb.save(membrane_nii, membrane_path)

    # Membrane Binning
    membrane_bin_path = data_path + 'mem_bin.nii'
    membrane_bin = np.absolute(matfile['image_membrane2gas_binned']) #pre-refactor 'bar2gas_binning' 

    # Put it in the correct orientation
    membrane_bin_transpose = np.transpose(membrane_bin, (1, 0, 2))

    # Make it into a nifti object
    membrane_bin_nii = nb.Nifti1Image(membrane_bin_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    membrane_bin_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])
    
    membrane_bin_nii.header.set_qform(None, code =2)

    # Save it as a file
    nb.save(membrane_bin_nii, membrane_bin_path)



    # EVERYTHING RBC 
    # Data
    rbc_path = data_path + 'rbc.nii'
    rbc = np.absolute(matfile['image_rbc2gas']) #pre-refactor name: 'rbc2gas'

    # Put it in the correct orientation
    rbc_transpose = np.transpose(rbc, (1, 0, 2))

    # Make it into a nifti object
    rbc_nii = nb.Nifti1Image(rbc_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    rbc_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])

    rbc_nii.header.set_qform(None, code = 2)

    # Save it as a file
    nb.save(rbc_nii, rbc_path) 

    # Bin
    rbc_bin_path = data_path + 'rbc_bin.nii'
    rbc_bin = np.absolute(matfile['image_rbc2gas_binned']) #pre-refactor name:'rbc2gas_binning'

    # Put it in the correct orientation
    rbc_bin_transpose = np.transpose(rbc_bin, (1, 0, 2))

    # Make it into a nifti object
    rbc_bin_nii = nb.Nifti1Image(rbc_bin_transpose.astype(float), np.eye(4))

    # Put the correct dimensions in the header 
    rbc_bin_nii.header['pixdim'] = np.array([1., 3.125, 3.125, 3.125, 0., 0., 0., 0.])

    rbc_bin_nii.header.set_qform(None, code = 2)

    # Save it as a file
    nb.save(rbc_bin_nii, rbc_bin_path) 

    return()
