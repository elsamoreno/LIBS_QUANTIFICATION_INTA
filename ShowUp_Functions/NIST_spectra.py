#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from astroquery.nist import Nist
import astropy.units as u

wl_min_UV1 = 236.381 * u.nm
wl_max_UV1 = 363.792 * u.nm
wl_min_UV2 = 353.533 * u.nm
wl_max_UV2 = 463.862 * u.nm
wl_min_VIS = 450.961 * u.nm
wl_max_VIS = 705.106 * u.nm
wl_min_NIR = 691.496 * u.nm
wl_max_NIR = 1056.420 * u.nm

def LIBS_over_NIST(dataUV1, dataUV2, dataVIS, dataNIR, Elems, IntensityThreshold):

    #Get wavelengths and intensity
    wls_UV1 = dataUV1['Wave']
    wls_UV2 = dataUV2['Wave']
    wls_VIS = dataVIS['Wave']
    wls_NIR = dataNIR['Wave']
    counts_UV1 = dataUV1['Sample']
    counts_UV2 = dataUV2['Sample']
    counts_VIS = dataVIS['Sample']
    counts_NIR = dataNIR['Sample']

    #Get peak wavelengths
    picos_UV1, propiedades = find_peaks(counts_UV1, prominence=1000,
                                                    height=1000,
                                                    distance=1)
    longitudes_pico_UV1 = wls_UV1[picos_UV1]
    counts_pico_UV1 = propiedades['peak_heights']

    picos_UV2, propiedades = find_peaks(counts_UV2, prominence=1000,
                                                    height=1000,
                                                    distance=1)
    longitudes_pico_UV2 = wls_UV2[picos_UV2]
    counts_pico_UV2 = propiedades['peak_heights']

    picos_VIS, propiedades = find_peaks(counts_VIS, prominence=1000,
                                                    height=1000,
                                                    distance=1)
    longitudes_pico_VIS = wls_VIS[picos_VIS]
    counts_pico_VIS = propiedades['peak_heights']

    picos_NIR, propiedades = find_peaks(counts_NIR, prominence=1000,
                                                    height=1000,
                                                    distance=1)
    longitudes_pico_NIR = wls_NIR[picos_NIR]
    counts_pico_NIR = propiedades['peak_heights']


    result1 = Nist.query(wl_min_UV1, wl_max_UV1, linename= Elems)
    filtered_result1 = result1[(result1["Spectrum"] == f"{Elems} I") | (result1["Spectrum"] == f"{Elems} II")]
    filtered_result1["Rel."] = pd.to_numeric(filtered_result1["Rel."], errors="coerce")
    filtered_result1 = filtered_result1[filtered_result1["Rel."] > IntensityThreshold]  # Ajusta el umbral según tu espectro

    result2 = Nist.query(wl_min_UV2, wl_max_UV2, linename= Elems)
    filtered_result2 = result2[(result2["Spectrum"] == f"{Elems} I") | (result2["Spectrum"] == f"{Elems} II")]
    filtered_result2["Rel."] = pd.to_numeric(filtered_result2["Rel."], errors="coerce")
    filtered_result2 = filtered_result2[filtered_result2["Rel."] > IntensityThreshold]  # Ajusta el umbral según tu espectro

    result3 = Nist.query(wl_min_VIS, wl_max_VIS, linename= Elems)
    filtered_result3 = result3[(result3["Spectrum"] == f"{Elems} I") | (result3["Spectrum"] == f"{Elems} II")]
    filtered_result3["Rel."] = pd.to_numeric(filtered_result3["Rel."], errors="coerce")
    filtered_result3 = filtered_result3[filtered_result3["Rel."] > IntensityThreshold]  # Ajusta el umbral según tu espectro

    result4 = Nist.query(wl_min_NIR, wl_max_NIR, linename= Elems)
    filtered_result4 = result4[(result4["Spectrum"] == f"{Elems} I") | (result4["Spectrum"] == f"{Elems} II")]
    filtered_result4["Rel."] = pd.to_numeric(filtered_result4["Rel."], errors="coerce")
    filtered_result4 = filtered_result4[filtered_result4["Rel."] > IntensityThreshold]  # Ajusta el umbral según tu espectro

    plt.figure(figsize=(10,5))
    plt.plot(wls_UV1, counts_UV1, label="Espectro LIBS", color="blue")
    plt.scatter(longitudes_pico_UV1, counts_pico_UV1, color="red", label = "picos detectados")

    #print(filtered_result)
    for wl in filtered_result1["Observed"]:
        plt.axvline(x = wl, color="orange", linestyle="--",alpha = 0.15, label= f"Líneas {Elems} NIST" if f"Líneas {Elems} NIST" not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.xlabel("Longitud de onda (mm)")
    plt.ylabel("Intensidad")
    plt.title("Ultraviolet 1")
    plt.legend()
    plt.show()


    plt.figure(figsize=(10,5))
    plt.plot(wls_UV2, counts_UV2, label="Espectro LIBS", color="blue")
    plt.scatter(longitudes_pico_UV2, counts_pico_UV2, color="red", label = "picos detectados")

    #print(filtered_result)
    for wl in filtered_result2["Observed"]:
        plt.axvline(x = wl, color="orange", linestyle="--",alpha = 0.15, label= f"Líneas {Elems} NIST" if f"Líneas {Elems} NIST" not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.xlabel("Longitud de onda (mm)")
    plt.ylabel("Intensidad")
    plt.title("Ultraviolet 2")
    plt.legend()
    plt.show()


    plt.figure(figsize=(10,5))
    plt.plot(wls_VIS, counts_VIS, label="Espectro LIBS", color="blue")
    plt.scatter(longitudes_pico_VIS, counts_pico_VIS, color="red", label = "picos detectados")

    #print(filtered_result)
    for wl in filtered_result3["Observed"]:
        plt.axvline(x = wl, color="orange", linestyle="--",alpha = 0.15, label= f"Líneas {Elems} NIST" if f"Líneas {Elems} NIST" not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.xlabel("Longitud de onda (mm)")
    plt.ylabel("Intensidad")
    plt.title("Visible")
    plt.legend()
    plt.show()


    plt.figure(figsize=(10,5))
    plt.plot(wls_NIR, counts_NIR, label="Espectro LIBS", color="blue")
    plt.scatter(longitudes_pico_NIR, counts_pico_NIR, color="red", label = "picos detectados")

    #print(filtered_result)
    for wl in filtered_result4["Observed"]:
        plt.axvline(x = wl, color="orange", linestyle="--",alpha = 0.15, label= f"Líneas {Elems} NIST" if f"Líneas {Elems} NIST" not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.xlabel("Longitud de onda (mm)")
    plt.ylabel("Intensidad")
    plt.title("Near-Infrarred")
    plt.legend()
    plt.show()


    return



def average_spectra(data_list):

    if not data_list:
        # Si la lista está vacía, devolver un DataFrame vacío con las columnas esperadas
        return pd.DataFrame(columns=["Wave", "Sample"])
    """
    Calcula el espectro promedio a partir de una lista de DataFrames de espectros.
    
    Parameters:
        data_list (list of pd.DataFrame): Lista con 5 DataFrames de espectros con columnas 'Wave' y 'Sample'.
    
    Returns:
        pd.DataFrame: DataFrame con la media de los espectros.
    """
    # Verificar que todos los DataFrames tienen las columnas correctas
    for i, df in enumerate(data_list):
        if not {"Wave", "Sample"}.issubset(df.columns):
            raise ValueError(f"El DataFrame {i+1} no tiene las columnas esperadas.")
    
    # Concatenar los DataFrames
    df_concat = pd.concat(data_list, ignore_index=True)

    # Asegurar que 'Wave' y 'Sample' son numéricos
    df_concat["Wave"] = pd.to_numeric(df_concat["Wave"], errors="coerce")
    df_concat["Sample"] = pd.to_numeric(df_concat["Sample"], errors="coerce")
    
    # Eliminar filas con valores NaN generados en la conversión
    df_concat = df_concat.dropna(subset=["Wave", "Sample"])

    # Agrupar por 'Wave' y calcular la media de 'Sample'
    df_avg = df_concat.groupby("Wave", as_index=False)["Sample"].mean()

    return df_avg
