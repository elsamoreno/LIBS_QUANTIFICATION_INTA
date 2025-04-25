### Offset correction function

def get_corrected_spectra(data_UV1, data_UV2, data_VIS, data_NIR):
    # Verificar que los DataFrames no están vacíos
    if any(df.empty for df in [data_UV1, data_UV2, data_VIS, data_NIR]):
        raise ValueError("Uno o más DataFrames están vacíos. No se puede aplicar la corrección.")

    wls_UV1 = data_UV1['Wave']
    wls_UV2 = data_UV2['Wave']
    wls_VIS = data_VIS['Wave']
    wls_NIR = data_NIR['Wave']
    
    # Overlapping intervals
    i1 = (wls_UV2.iloc[1], wls_UV1.iloc[-1])
    i2 = (wls_VIS.iloc[1], wls_UV2.iloc[-1])
    i3 = (wls_NIR.iloc[1], wls_VIS.iloc[-1])
    
    # Overlapping intervals isolation
    data_UV1_fil1 = data_UV1[(data_UV1['Wave'] >= i1[0]) & (data_UV1['Wave'] <= i1[1])]
    data_UV2_fil1 = data_UV2[(data_UV2['Wave'] >= i1[0]) & (data_UV2['Wave'] <= i1[1])]
    data_UV2_fil2 = data_UV2[(data_UV2['Wave'] >= i2[0]) & (data_UV2['Wave'] <= i2[1])]
    data_VIS_fil2 = data_VIS[(data_VIS['Wave'] >= i2[0]) & (data_VIS['Wave'] <= i2[1])]
    data_VIS_fil3 = data_VIS[(data_VIS['Wave'] >= i3[0]) & (data_VIS['Wave'] <= i3[1])]
    data_NIR_fil3 = data_NIR[(data_NIR['Wave'] >= i3[0]) & (data_NIR['Wave'] <= i3[1])]

    # Verificar que todos los subconjuntos tienen datos
    filtros = {
        'UV1_fil1': data_UV1_fil1, 'UV2_fil1': data_UV2_fil1,
        'UV2_fil2': data_UV2_fil2, 'VIS_fil2': data_VIS_fil2,
        'VIS_fil3': data_VIS_fil3, 'NIR_fil3': data_NIR_fil3
    }
    for nombre, df in filtros.items():
        if df.empty:
            raise ValueError(f"El filtro '{nombre}' no contiene datos. No se puede calcular la corrección.")

    # Medians calculus
    median_UV1_fil1 = data_UV1_fil1['Sample'].median()
    median_UV2_fil1 = data_UV2_fil1['Sample'].median()
    median_UV2_fil2 = data_UV2_fil2['Sample'].median()
    median_VIS_fil2 = data_VIS_fil2['Sample'].median()
    median_VIS_fil3 = data_VIS_fil3['Sample'].median()
    median_NIR_fil3 = data_NIR_fil3['Sample'].median()

    # Verificar que no hay división por cero
    if median_UV2_fil1 == 0 or median_VIS_fil2 == 0 or median_NIR_fil3 == 0:
        raise ZeroDivisionError("Una de las medianas utilizadas para calcular los coeficientes es cero.")

    # Coefficients calculus
    coef1 = median_UV1_fil1 / median_UV2_fil1
    coef2 = median_UV2_fil2 / median_VIS_fil2
    coef3 = median_VIS_fil3 / median_NIR_fil3

    # Apply coefficients
    data_UV1_corr = data_UV1.copy()
    data_UV2_corr = data_UV2.copy()
    data_VIS_corr = data_VIS.copy()
    data_NIR_corr = data_NIR.copy()

    data_UV1_corr['Sample'] = data_UV1_corr['Sample']
    data_UV2_corr['Sample'] = data_UV2_corr['Sample'] * coef1
    data_VIS_corr['Sample'] = data_VIS_corr['Sample'] * coef2 * coef1
    data_NIR_corr['Sample'] = data_NIR_corr['Sample'] * coef3 * coef2 * coef1

    return data_UV1_corr, data_UV2_corr, data_VIS_corr, data_NIR_corr
