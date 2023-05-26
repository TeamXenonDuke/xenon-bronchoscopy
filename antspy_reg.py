# Function ants_reg

def ants_pyreg(reg_type, vent_mask_path, ct_whole_path, output_path):
   
    import os 
    import antspy
    
    sublobe_whole_reg_path = output_path + 'sublobe_whole_reg.nii'
    sublobe_transpose_path = output_path + 'sublobe_transpose.nii'
    sublobe_reg_path = output_path + 'sublobe_transpose_reg.nii'
    ct_path = output_path + 'ct.nii'
    ct_reg_path = output_path + 'ct_reg.nii'

    if reg_type == 1:

        
       

    elif reg_type == 2:
        cmd_syn_withmask = ('./antsRegistration -d 3 -verbose 1 '
            '-o [syn_deform_matrix, '+sublobe_whole_reg_path+'] -n BSpline '
            '-r ['+vent_mask_path+', '+ct_whole_path+',2] '
            '-t Rigid[0.15] '
            '-m MI['+vent_mask_path+', '+ct_whole_path+', 1, 32, Regular, 1] '
            '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 '
            '-t Affine[0.25] '
            '-m MI['+vent_mask_path+', '+ct_whole_path+', 1, 32, Regular, 1] '
            '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 '
            '-t Syn[0.1, 3.0, 0] '
            '-m MI['+vent_mask_path+', '+ct_whole_path+', 1, 32, Regular, 1] '
            '-c [1000x500x500x500, 1e-8, 10] -f 8x4x2x1 -s 0x0x0x0 ')

        cmd_syn_withmask_simple = ('./antsRegistration -d 3 -verbose 1 '
            '-o [syn_deform_matrix, '+sublobe_whole_reg_path+'] -n BSpline '
            '-r ['+vent_mask_path+', '+ct_whole_path+',2] '
            '-t Rigid[0.15] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 4] '
            '-c [500x500x500, 1e-8, 10] -f 4x2x1 -s 0x0x0 '
            '-t Affine[0.25] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 4] '
            '-c [500x500x500, 1e-8, 10] -f 4x2x1 -s 0x0x0 '
            '-t Syn[0.25, 3.0, 0.05] '
            '-m CC['+vent_mask_path+', '+ct_whole_path+', 1, 4] '
            '-c [500x500x500, 1e-8, 10] -f 4x2x1 -s 0x0x0 ')


        # Calculate Dice score? 

        
        os.system(cmd_syn_withmask_simple)
        print('CT-Gas Registration Completed')


    # Apply transform to sublobe mask
    cmd_apply = ('./antsApplyTransforms -d 3 '
            '-i ' +sublobe_transpose_path+ ' '
            '-o ' +sublobe_reg_path+ ' '
            '-n multilabel '
            '-r '+vent_mask_path+' '
            '-t [syn_deform_matrix0GenericAffine.mat, 0] '
            '-t syn_deform_matrix1Warp.nii.gz ')

    os.system(cmd_apply)

    # And to CT

    cmd_apply_ct = ('./antsApplyTransforms -d 3 '
            '-i ' +ct_path+ ' '
            '-o ' +ct_reg_path+ ' '
            '-n linear '
            '-r '+vent_mask_path+ ' '
            '-t [syn_deform_matrix0GenericAffine.mat, 0] '
            '-t syn_deform_matrix1Warp.nii.gz ')

    os.system(cmd_apply_ct)

    
    return()