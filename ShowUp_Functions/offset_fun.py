### Offset correction function

def get_corrected_spectra(data_UV1, data_UV2, data_VIS, data_NIR):
    wls_UV1 = data_UV1['Wave']
    wls_UV2 = data_UV2['Wave']
    wls_VIS = data_VIS['Wave']
    wls_NIR = data_NIR['Wave']
    #Overlapping intervals
    i1 = (wls_UV2[1], wls_UV1[len(wls_UV1)-1])
    i2 = (wls_VIS[1], wls_UV2[len(wls_UV2)-1])
    i3 = (wls_NIR[1], wls_VIS[len(wls_VIS)-1])
    #Overlapping intervals isolation
    data_UV1_fil1 = data_UV1[(data_UV1['Wave'] >= i1[0]) & (data_UV1['Wave'] <= i1[1])]
    data_UV2_fil1 = data_UV2[(data_UV2['Wave'] >= i1[0]) & (data_UV2['Wave'] <= i1[1])]
    data_UV2_fil2 = data_UV2[(data_UV2['Wave'] >= i2[0]) & (data_UV2['Wave'] <= i2[1])]
    data_VIS_fil2 = data_VIS[(data_VIS['Wave'] >= i2[0]) & (data_VIS['Wave'] <= i2[1])]
    data_VIS_fil3 = data_VIS[(data_VIS['Wave'] >= i3[0]) & (data_VIS['Wave'] <= i3[1])]
    data_NIR_fil3 = data_NIR[(data_NIR['Wave'] >= i3[0]) & (data_NIR['Wave'] <= i3[1])]
    #Medians calculus
    median_UV1_fil1 = data_UV1_fil1['Sample'].median()
    median_UV2_fil1 = data_UV2_fil1['Sample'].median()
    median_UV2_fil2 = data_UV2_fil2['Sample'].median()
    median_VIS_fil2 = data_VIS_fil2['Sample'].median()
    median_VIS_fil3 = data_VIS_fil3['Sample'].median()
    median_NIR_fil3 = data_NIR_fil3['Sample'].median()
    #Coefficients calculus
    coef1 = median_UV1_fil1/median_UV2_fil1
    coef2 = median_UV2_fil2/median_VIS_fil2
    coef3 = median_VIS_fil3/median_NIR_fil3
    #Apply coefficients
    data_UV1_corr = data_UV1.copy()
    data_UV2_corr = data_UV2.copy()
    data_VIS_corr = data_VIS.copy()
    data_NIR_corr = data_NIR.copy()
    data_UV1_corr['Sample'] = data_UV1_corr['Sample']
    data_UV2_corr['Sample'] = data_UV2_corr['Sample']*coef1
    data_VIS_corr['Sample'] = data_VIS_corr['Sample']*coef2*coef1
    data_NIR_corr['Sample'] = data_NIR_corr['Sample']*coef3*coef2*coef1
    return data_UV1_corr,data_UV2_corr,data_VIS_corr,data_NIR_corr
