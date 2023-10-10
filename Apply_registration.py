# Set Flags
im_to_apply_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/sublobe_transpose.nii'
fixed_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/dedvent_mask.nii'
output_im_path = '/mnt/c/Users/Asia/OneDrive/Pulpit/Team_Xenon/Xenon_data/registration_playground/OS_17/apply_backwards_reg_SyN_from_sublobe_transpose.nii'
reg_type = 3 #1 - Rigid, #2 - Affine, #3 - Syn
label = 'multiLabel' #multiLabel , #linear - if applying to ct?
direction = "backwards" #forward, #backwards

def apply_registration(im_to_apply_path, fixed_im_path, output_im_path, reg_type, label, direction):
   
    import os 
    import numpy as np
    import nibabel as nb
    import pdb


    if direction == 'forward':
        if reg_type == 1:
            cmd_apply = ('./antsApplyTransforms -d 3 '
                '-i ' +im_to_apply_path+ ' '
                '-o ' +output_im_path+ ' '
                '-n ' +label+ ' '
                '-r ' +fixed_im_path+ ' '
                '-t rigid_deform_matrix0GenericAffine.mat '
                ) 
            
            os.system(cmd_apply)
            print('Applying forward rigid registration completed')

        if reg_type in [2, 3]:
            cmd_apply = ('./antsApplyTransforms -d 3 '
                '-i ' +im_to_apply_path+ ' '
                '-o ' +output_im_path+ ' '
                '-n ' +label+ ' '
                '-r '+fixed_im_path+' '
                '-t syn_deform_matrix1Warp.nii.gz '
                '-t syn_deform_matrix0GenericAffine.mat '
                )    
            
            os.system(cmd_apply)
            print('Applying forward SyN registration completed')

    if direction =='backwards':
        if reg_type == 3:
            cmd_apply = ('./antsApplyTransforms -d 3 '
                '-i ' +fixed_im_path+ ' '
                '-o ' +output_im_path+ ' '
                '-n ' +label+ ' '
                '-r '+im_to_apply_path+' '
                '-t syn_deform_matrix1InverseWarp.nii.gz '
                '-t syn_deform_matrix0GenericAffine.mat '
                )    
            
            os.system(cmd_apply)
            print('Applying backwards SyN registration completed')



    # Calculate Dice score

    # Load in fixed mask & get image
    if direction == 'forward':
        vent_mask_nii = nb.load(fixed_im_path)
    if direction == 'backwards':
        vent_mask_nii = nb.load(im_to_apply_path)
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
    print("Dice score: "+ str(round(dice_score,3)))


    return()

apply_registration(im_to_apply_path, fixed_im_path, output_im_path, reg_type, label, direction)