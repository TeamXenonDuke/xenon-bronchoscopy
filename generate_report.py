# Generate Bronch Report Numbers
# Begun by David Mummy 5/18/21

def generate_report(processing_path, subject_id, flavor, dedvent_mask_path, dedvent_bin_path):

    import nibabel as nb
    import numpy as np
    import csv
    import pdb

    # Load data
    sublobe_path = processing_path + 'sublobe_transpose_reg.nii'

    sublobe = nb.load(sublobe_path)
    dedvent_mask = nb.load(dedvent_mask_path)
    dedvent_bin = nb.load(dedvent_bin_path)

    sublobe_img = sublobe.get_fdata()
    dedvent_mask_img = dedvent_mask.get_fdata()
    dedvent_bin_img = dedvent_bin.get_fdata()

    sublobe_array = sublobe_img.flatten()
    dedvent_mask_array = dedvent_mask_img.flatten()
    dedvent_bin_array = dedvent_bin_img.flatten() - 1

    # But we only want values within the lung

    sublobe_tcv = sublobe_array[dedvent_mask_array == 1]
    dedvent_tcv = dedvent_bin_array[dedvent_mask_array == 1]


    # Get sublobe values & length of array
    sublobe_values = np.unique(sublobe_array)
    sublobe_values_len = len(sublobe_values)

    # open CSV for writing
    
    filename = 'sublobe_'+subject_id+'_'+flavor+'.csv'
    
    with open(processing_path + filename, 'w', newline = '') as csvfile:
        csv_write = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        csv_write.writerow(['subject_id', 'flavor', 'region', 'bin1', 'bin2', 'bin3', 'bin4', 'bin5', 'bin6', 'bin7', 'bin8'])

    # Populate lookup table
    sublobe_lookup = [None]*255
    sublobe_lookup[1] = 'LB1'
    sublobe_lookup[2] = 'LB2'
    sublobe_lookup[3] = 'LB3'
    sublobe_lookup[4] = 'LB4'
    sublobe_lookup[5] = 'LB5'
    sublobe_lookup[6] = 'LB1_2'
    sublobe_lookup[7] = 'LB4_5'
    sublobe_lookup[102] = 'LB6'
    sublobe_lookup[104] = 'LB8'
    sublobe_lookup[105] = 'LB9'
    sublobe_lookup[106] = 'LB10'
    sublobe_lookup[129] = 'RB1'
    sublobe_lookup[130] = 'RB2'
    sublobe_lookup[131] = 'RB3'
    sublobe_lookup[164] = 'RB4'
    sublobe_lookup[165] = 'RB5'
    sublobe_lookup[230] = 'RB6'
    sublobe_lookup[231] = 'RB7'
    sublobe_lookup[232] = 'RB8'
    sublobe_lookup[233] = 'RB9'
    sublobe_lookup[234] = 'RB10'
    sublobe_lookup[8]   = 'ucLUL'
    sublobe_lookup[16]  = 'ucLLL'
    sublobe_lookup[32]  = 'ucRUL'
    sublobe_lookup[64]  = 'ucRML'
    sublobe_lookup[128] = 'ucRLL'

    #OUTPUT METRICS

    left_lung_array = [1,2,3,4,5,6,7,102,104,105,106,8,16]
    right_lung_array = [129,130,131,164,165,230,231,232,233,234,32,64,128]

    part = ["whole", 'left', 'right', 'RUL', 'RML', 'RLL', 'LUL', 'LLL' ]
    for i in part:
        if i == "whole":
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element != 0] #we want to take the whole area of the lungs from sublobe_tcv so all the values except 0 (the background)

        if i == "left":
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element in left_lung_array]

        if i == "right":
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element in right_lung_array]

        if i == 'RUL':  #RUL (Right Upper Lobe): RB1 + RB2 + RB3
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element == 129 or element == 130 or element == 131 or element == 32]

        if i == 'RML':  #RML (Right Middle Lobe): RB4 + RB5
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element == 164 or element == 165 or element == 64]

        if i == "RLL":  #RLL (Right Lower Lobe): RB6 + RB7 + RB8 + RB9 + RB10
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element == 230 or element == 231 or element == 232 or element == 233 or element == 234 or element == 128]

        if i == "LUL":  #LUL (Left Upper Lobe): LB1 + LB2 + LB3 + LB4 + LB5
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element == 1 or element == 2 or element == 3 or element == 4 or element == 5 or element == 6 or element == 7 or element == 8]

        if i == 'LLL':  #LLL (Left Lower Lobe): LB6 + LB8 + LB9 + LB10
            dedvent_subset = [dedvent_tcv[i] for i, element in enumerate(sublobe_tcv) if element == 102 or element == 104 or element == 105 or element == 106 or element == 16]
    
        dedvent_subset_len = len(dedvent_subset)

        dedvent_bin1 = dedvent_subset.count(1)
        dedvent_bin1_pct = dedvent_bin1/dedvent_subset_len*100

        dedvent_bin2 = dedvent_subset.count(2)
        dedvent_bin2_pct = dedvent_bin2/dedvent_subset_len*100

        dedvent_bin3 = dedvent_subset.count(3)
        dedvent_bin3_pct = dedvent_bin3/dedvent_subset_len*100

        dedvent_bin4 = dedvent_subset.count(4)
        dedvent_bin4_pct = dedvent_bin4/dedvent_subset_len*100

        dedvent_bin5 = dedvent_subset.count(5)
        dedvent_bin5_pct = dedvent_bin5/dedvent_subset_len*100

        dedvent_bin6 = dedvent_subset.count(6)
        dedvent_bin6_pct = dedvent_bin6/dedvent_subset_len*100

        dedvent_bin7 = dedvent_subset.count(7)
        dedvent_bin7_pct = dedvent_bin7/dedvent_subset_len*100

        dedvent_bin8 = dedvent_subset.count(8)
        dedvent_bin8_pct = dedvent_bin8/dedvent_subset_len*100

        checksum = dedvent_bin1_pct + dedvent_bin2_pct + dedvent_bin3_pct + dedvent_bin4_pct + dedvent_bin5_pct + dedvent_bin6_pct + dedvent_bin7_pct + dedvent_bin8_pct
        print('For ' + i + '  this number should be 100%: ' +str(round(checksum,2))+'%')
        
        with open(processing_path + filename, 'a', newline = '') as csvfile:
            csv_write = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
            #csv_write.writerow(['subject_id', 'flavor', 'region', 'bin1', 'bin2', 'bin3', 'bin4', 'bin5', 'bin6', 'bin7', 'bin8'])
            csv_write.writerow([subject_id, flavor, i, round(dedvent_bin1_pct,3), round(dedvent_bin2_pct,3), round(dedvent_bin3_pct,3), round(dedvent_bin4_pct,3), round(dedvent_bin5_pct,3), round(dedvent_bin6_pct,3), round(dedvent_bin7_pct,3), round(dedvent_bin8_pct,3)])



    for x in sublobe_values:

        i = int(x)

        # is this just a silly extra step? No, because we still have to define the subset in addition to getting its length   
        dedvent_subset = dedvent_tcv[sublobe_tcv == i]
        dedvent_subset_len = len(dedvent_subset)

        #print('Seg ' + str(sublobe_lookup[i]) + ' is ' + str(round(dedvent_subset_len/len(dedvent_tcv)*100,1)) + '% of the total TCV')


        dedvent_bin1 = np.count_nonzero(dedvent_subset == 1)
        dedvent_bin1_pct = dedvent_bin1/dedvent_subset_len*100
        #print('VDP for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin1_pct,1)))

        dedvent_bin2 = np.count_nonzero(dedvent_subset == 2)
        dedvent_bin2_pct = dedvent_bin2/dedvent_subset_len*100
        #print('LVP for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin2_pct,1)))

        dedvent_vdp_lvp_pct = dedvent_bin1_pct + dedvent_bin2_pct
        #print('VDP + LVP for seg ' +str(sublobe_lookup[i]) + ' is ' + str(round(dedvent_vdp_lvp_pct, 1)))

        dedvent_bin3 = np.count_nonzero(dedvent_subset == 3)
        dedvent_bin3_pct = dedvent_bin3/dedvent_subset_len*100
        #print('bin3 for seg ' +str(sublobe_lookup[i])+' is ' + str(round(dedvent_bin3_pct,1)))

        dedvent_bin4 = np.count_nonzero(dedvent_subset == 4)
        dedvent_bin4_pct = dedvent_bin4/dedvent_subset_len*100
        #print('bin4 for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin4_pct,1)))

        dedvent_bin5 = np.count_nonzero(dedvent_subset == 5)
        dedvent_bin5_pct = dedvent_bin5/dedvent_subset_len*100
        #print('bin5 for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin5_pct,1)))

        dedvent_bin6 = np.count_nonzero(dedvent_subset == 6)
        dedvent_bin6_pct = dedvent_bin6/dedvent_subset_len*100
        #print('bin6 for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin6_pct,1)))

        dedvent_bin7 = np.count_nonzero(dedvent_subset == 7)
        dedvent_bin7_pct = dedvent_bin7/dedvent_subset_len*100
        #print('bin6 for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin6_pct,1)))

        dedvent_bin8 = np.count_nonzero(dedvent_subset == 8)
        dedvent_bin8_pct = dedvent_bin8/dedvent_subset_len*100
        #print('bin7 for seg ' +str(sublobe_lookup[i])+ ' is ' + str(round(dedvent_bin6_pct,1)))

        checksum = dedvent_bin1_pct + dedvent_bin2_pct + dedvent_bin3_pct + dedvent_bin4_pct + dedvent_bin5_pct + dedvent_bin6_pct + dedvent_bin7_pct + dedvent_bin8_pct

        with open(processing_path + filename, 'a', newline = '') as csvfile:
            csv_write = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
            csv_write.writerow([subject_id, flavor, str(sublobe_lookup[i]), round(dedvent_bin1_pct,3), round(dedvent_bin2_pct,3), round(dedvent_bin3_pct,3), round(dedvent_bin4_pct,3), round(dedvent_bin5_pct,3), round(dedvent_bin6_pct,3), round(dedvent_bin7_pct,3), round(dedvent_bin8_pct,3)])
            
            # Use CSV write function to start on new line in csv file

        # Need to do better error checking here. Break out of this loop to get total sums of volumes etc. Do the parts properly add up to the whole? 
        print('For vent, this number should be 100%: ' +str(round(checksum,2))+'%')


    whole_lung_vdp = len(dedvent_tcv[dedvent_tcv == 1])/len(dedvent_tcv)
    print('Whole lung Defect check: ' + str(round(whole_lung_vdp*100,1)))

    whole_lung_lvp = len(dedvent_tcv[dedvent_tcv == 2])/len(dedvent_tcv)
    print('Whole lung Low check: ' + str(round(whole_lung_lvp*100,1)))

    print('Whole lung vent volume check: ' + str(round(len(dedvent_tcv)*3.125**3/10**6,2)) + 'L')

    dedvent_uncovered = dedvent_tcv[sublobe_tcv == 0]
    print('Vent volume outside CT: ' + str(round(len(dedvent_uncovered)*3.125**3/10**6,2)) + 'L')
    print('\n')
    #print('CT-Covered Vent Volume:
    
    return()
