
# SET FLAGS

#moving image path
moving_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/ct_whole_lung_mask.nii'
#fixed image path
fixed_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/dedvent_mask.nii'
#output image path
output_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/output_im_reg_affine.nii'
#rest of the flags
reg_type = 2 #1 - Rigid, #2 - Affine, #3 - Syn
label = 'multiLabel' #multiLabel - use if registering masks, #linear

def registration(moving_im_path, fixed_im_path, output_im_path, reg_type, label):
   
    import os 
    import numpy as np
    import nibabel as nb

    if reg_type == 1:

        cmd_rigid = ('./antsRegistration -d 3 --verbose 1 '
            '-o [rigid_deform_matrix, '+output_im_path+'] -n BSpline '
            '-r ['+fixed_im_path+', '+moving_im_path+',1] '
            '-t Rigid[0.15] '
            '-m MI['+fixed_im_path+', '+moving_im_path+', 1, 32, Regular, 1] '
            '-c [100x40x20, 1e-6, 10] -f 4x2x1 -s 0x0x0 '
            '-n ' +label+ ' '
            )

        os.system(cmd_rigid)
        print('Rigid registration completed')

    elif reg_type == 2:
       
        cmd_affine = ('./antsRegistration -d 3 --verbose 1 '
            '-o [affine_deform_matrix, '+output_im_path+'] -n BSpline '
            '-r ['+fixed_im_path+', '+moving_im_path+',1] '
            '-t Rigid[0.15] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50, 1e-6, 10] -f 4x2 -s 4x2 '
            '-t Affine[0.4] '
            '-m CC['+fixed_im_path+', '+moving_im_path+', 1, 2] '
            '-c [100x50x25, 1e-6, 10] -f 4x2x1 -s 4x2x1 '
            '-n ' +label+ ' '
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
            '-n ' +label+ ' '
            )

        os.system(cmd_syn)
        print('SyN registration completed')


    # Calculate Dice score

    # Load in fixed im & get image
    fixed_im_nii = nb.load(fixed_im_path)
    fixed_mask = fixed_im_nii.get_fdata()
    fixed_mask_array = fixed_mask.flatten()

    # Load in registered output image
    output_im_nii = nb.load(output_im_path)
    output_im = output_im_nii.get_fdata()
    output_im_array = output_im.flatten()

    
     
    #DICE SCORE CALCULATION
    #common part
    sublobe_tcv1 = output_im_array[fixed_mask_array == 1] #taking part of the output im array in a shape of the fixed image array
    common_part = np.count_nonzero(sublobe_tcv1) #calculating the common part of the two masks
    dice_score = 2*common_part/((np.count_nonzero(fixed_mask_array)+np.count_nonzero(output_im_array)))
    # Output dice score
    print("\nHere is where the Dice score would be calculated\n")
    print("Dice score: "+ str(round(dice_score,4)))


    return()


registration(moving_im_path, fixed_im_path, output_im_path, reg_type, label)