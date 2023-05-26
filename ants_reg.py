# Function ants_reg

def ants_reg(reg_type, vent_mask_path, ct_whole_path, output_path):
   
    import os 
    import numpy as np
    import nibabel as nb
    import pdb

    sublobe_whole_reg_path = output_path + 'sublobe_whole_reg.nii'
    sublobe_transpose_path = output_path + 'sublobe_transpose.nii'
    sublobe_reg_path = output_path + 'sublobe_transpose_reg.nii'
    ct_path = output_path + 'ct.nii'
    ct_reg_path = output_path + 'ct_reg.nii'

    if reg_type == 1:

        cmd_rigid = ('./antsRegistration -d 3 -verbose 1 '
            '-o [rigid_deform_matrix, '+sublobe_whole_reg_path+'] -n BSpline '
            '-r ['+vent_mask_path+', '+ct_whole_path+',2] '
            '-t Rigid[0.15] '
            '-m MI['+vent_mask_path+', '+ct_whole_path+', 1, 32, Regular, 1] '
            '-c [100x40x20, 1e-6, 10] -f 4x2x1 -s 0x0x0 '
            '-n multiLabel'
            )

        os.system(cmd_rigid)
        print('Rigid registration complete')

    elif reg_type == 2:
       
        cmd_syn_withmask_simple = ('./antsRegistration -d 3 -verbose 1 '
            '-o [syn_deform_matrix, '+sublobe_whole_reg_path+'] -n BSpline '
            '-r ['+vent_mask_path+', '+ct_whole_path+',2] '
            '-t Rigid[0.15] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 2] '
            '-c [100x50, 1e-6, 10] -f 4x2 -s 4x2 '
            '-t Affine[0.4] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 2] '
            '-c [100x50x25, 1e-6, 10] -f 4x2x1 -s 4x2x1 '
            '-t Syn[0.4, 3.0, 0.1] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 2] '
            '-c [50x25x10, 1e-8, 10] -f 4x2x1 -s 4x2x1 '
            '-n multiLabel'
            )

       
        
        os.system(cmd_syn_withmask_simple)
        print('CT-Gas Registration Completed')

    # THIS WILL NOT WORK FOR THE RIGID REGISTRATION OPTION. Transforms not applied in this case. 
    if reg_type in [2, 3]:
        # Apply transform to sublobe mask
        cmd_apply = ('./antsApplyTransforms -d 3 '
            '-i ' +sublobe_transpose_path+ ' '
            '-o ' +sublobe_reg_path+ ' '
            '-n multilabel '
            '-r '+vent_mask_path+' '
            '-t syn_deform_matrix1Warp.nii.gz '
            '-t syn_deform_matrix0GenericAffine.mat '
            )       

        os.system(cmd_apply)

    # And to CT

        cmd_apply_ct = ('./antsApplyTransforms -d 3 '
            '-i ' +ct_path+ ' '
            '-o ' +ct_reg_path+ ' '
            '-n linear '
            '-r '+vent_mask_path+ ' '
            '-t syn_deform_matrix1Warp.nii.gz '
            '-t syn_deform_matrix0GenericAffine.mat '
            
            )

        os.system(cmd_apply_ct)

    # Calculate Dice score

    # Load in fixed mask & get image
    vent_mask_nii = nb.load(vent_mask_path)
    vent_mask = vent_mask_nii.get_fdata()
    # Convert this to Boolean
    vent_mask_bool = np.array(vent_mask, dtype = bool)

    # Load in registered whole lung sublobe mask
    sublobe_whole_reg_nii = nb.load(sublobe_whole_reg_path)
    sublobe_whole_reg = sublobe_whole_reg_nii.get_fdata()


   # pdb.set_trace() 
     
    # Output dice score
    print("\nHere is where the Dice score would be calculated\n")

    return()