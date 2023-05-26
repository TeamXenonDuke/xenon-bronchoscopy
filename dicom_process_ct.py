# FUNCTION dicom_process to read in a DICOM folder, grab dimensions from the header,
# and spit out a NIFTI image stack file
# Import arguments are a path to the dicoms and the desired path for niftis
def dicom_process_ct(dicom_path, nii_path):

    import numpy
    import pydicom
    import os
    import nibabel
    import pdb

    # Grab any files in the target folder that end in .dcm (might have to change this in future
    # if files don't have that extension)
    files = [os.path.join(dicom_path, fname)
        for fname in os.listdir(dicom_path) if fname.startswith('0')]

    # Sort files by file name
    files.sort()

    # Import first DICOM in series to get reference header dimensions
    ref_header = pydicom.dcmread(files[0])

    # Get pixel dimensions: cols, rows, number of files to indicate number of slices
    pixel_dims = (int(ref_header.Columns), int(ref_header.Rows), len(files))
    #pdb.set_trace()
    # Get voxel dimensions. NOTE: Assume in-plane dimensions are the same in CT acquisition

    # Axial acquisition
    voxel_dims = (float(ref_header.PixelSpacing[0]), float(ref_header.SliceThickness), float(ref_header.PixelSpacing[1]))

    # Coronal acquisition
   # voxel_dims = (float(ref_header.PixelSpacing[0]), float(ref_header.PixelSpacing[1]), float(ref_header.SliceThickness))



    # Initialize array of zeros with the dimensions indicated by pixel_dims
    dicom_import = numpy.zeros(pixel_dims)

    for filename in files:

        # read each dicom file-by-file and plop it into the dicom array
        dicom_slice = pydicom.read_file(filename)

        slice_no = int(dicom_slice[0x20,0x13].value) - 1
    #    dicom_import[:, :, files.index(filename)] = numpy.transpose(dicom_slice.pixel_array,(1,0))
        dicom_import[:, :, slice_no] = numpy.transpose(dicom_slice.pixel_array,(1,0))

    # AXIAL VIEW: Transpose the HECK out of it to get coronal view
    dicom_import_transpose = numpy.transpose(dicom_import, (0,2,1))
    
    # Coronal acquisition
    #dicom_import_transpose = dicom_import

    # get min and max, normalize
    array_min = numpy.min(dicom_import_transpose)
    array_max = numpy.max(dicom_import_transpose)
    array_range = array_max - array_min

    dicom_import_norm = (dicom_import_transpose - array_min)/array_range

    # Create a preliminary nifti object with dicom data
    nii_pre = nibabel.Nifti1Image(dicom_import_norm.astype(float), numpy.eye(4))


    # Grab the header from nii_pre to use as a template, and set dimensions to voxel_dims
    meta = nii_pre.header
    meta['pixdim'][1:4] = voxel_dims
    meta.set_qform(None,code=2)

    # Create final nifti object now with the proper header (I'm sure there's a better way to do this)
    nii = nibabel.Nifti1Image(dicom_import_norm.astype(float), numpy.eye(4), meta)
    nii_raw = nibabel.Nifti1Image(dicom_import_transpose.astype(float) - 1024, numpy.eye(4), meta)


    # Save it as a file
    nibabel.save(nii, nii_path)
    #nibabel.save(nii_raw, nii_path + '_raw.nii')

    # End function, return nifti object
    print('Imported DICOMs from '+dicom_path+' and saved to a nifti. Way to go!')
    return(nii)
