
# Set Flags
moving_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/ct_whole_lung_mask.nii'
fixed_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/dedvent_mask.nii'
output_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/output_im_reg_affine.nii'
reg_type = 2 #1 - Rigid, #2 - Affine, #3 - Syn

def registration(moving_im_path, fixed_im_path, output_im_path, reg_type):
   
    import os 
    import numpy as np
    import nibabel as nb
    import pdb

    if reg_type == 1:

        cmd_rigid = ('./antsRegistration -d 3 --verbose 1 '
            '-o [rigid_deform_matrix, '+output_im_path+'] -n BSpline '
            '-r ['+fixed_im_path+', '+moving_im_path+',1] '
            '-t Rigid[0.15] '
            '-m MI['+fixed_im_path+', '+moving_im_path+', 1, 32, Regular, 1] '
            '-c [100x40x20, 1e-6, 10] -f 4x2x1 -s 0x0x0 '
            '-n multiLabel'
            )

        os.system(cmd_rigid)
        print('Rigid registration completed')

    elif reg_type == 2:
       
        cmd_affine = ('./antsRegistration -d 3 --verbose 1 '
            '-o [syn_deform_matrix, '+output_im_path+'] -n BSpline '
            '-r ['+fixed_im_path+', '+moving_im_path+',1] '
            '-t Rigid[0.15] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50, 1e-6, 10] -f 4x2 -s 4x2 '
            '-t Affine[0.4] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50x25, 1e-6, 10] -f 4x2x1 -s 4x2x1 '
            '-n multiLabel'
            )
        
        os.system(cmd_affine)
        print('Affine registration completed')

    elif reg_type == 3:
       
        cmd_syn = ('./antsRegistration -d 3 --verbose 1 '
            '-o [syn_deform_matrix, '+output_im_path+'] -n BSpline '
            '-r ['+fixed_im_path+', '+moving_im_path+',1] '
            '-t Rigid[0.15] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50, 1e-6, 10] -f 4x2 -s 4x2 '
            '-t Affine[0.4] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50x25, 1e-6, 10] -f 4x2x1 -s 4x2x1 '
            '-t Syn[0.4, 3.0, 0.1] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [500x250x100, 1e-8, 10] -f 4x2x1 -s 4x2x1 '
            '-n multiLabel'
            )

        os.system(cmd_syn)
        print('SyN registration completed')


    # Calculate Dice score

    # Load in fixed im & get image
    vent_mask_nii = nb.load(fixed_im_path)
    vent_mask = vent_mask_nii.get_fdata()
    vent_mask_array = vent_mask.flatten()
    # Convert this to Boolean
    vent_mask_bool = np.array(vent_mask, dtype = bool)

    # Load in registered whole lung sublobe mask
    sublobe_whole_reg_nii = nb.load(output_im_path)
    sublobe_whole_reg = sublobe_whole_reg_nii.get_fdata()
    sublobe_whole_reg_array = sublobe_whole_reg.flatten()

   # pdb.set_trace() 
     
    #DICE SCORE CALCULATION
    #common part
    sublobe_tcv1 = sublobe_whole_reg_array[vent_mask_array == 1] #taking part of the sublobe array in a shape of the ventilation mask
    common_part = np.count_nonzero(sublobe_tcv1) #calculating the common part of the sublobe array and ventilation mask array
    dice_score = 2*common_part/((np.count_nonzero(vent_mask_array)+np.count_nonzero(sublobe_whole_reg_array)))
    # Output dice score
    print("\nHere is where the Dice score would be calculated\n")
    print("Dice score: "+ str(round(dice_score,5)))


    return()


registration(moving_im_path, fixed_im_path, output_im_path, reg_type)