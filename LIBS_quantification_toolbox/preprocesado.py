# -*- coding: utf-8 -*-
"""
lib_s_preprocessing.py

A user‑friendly, self‑contained pipeline for preprocessing raw LIBS spectral segments.
Each step is documented and exposes only the key parameters, so users can easily
customize without dealing with internal details.

Pipeline steps:
 1) Wavelet denoising (stationary transform + sigma clipping)
 2) Segment stitching (UV1, UV2, VIS, NIR groups)
 3) Robust baseline subtraction (local weighted regression + Tukey biweight)
 4) Trim to valid wavelength ranges for each segment
 5) Continuum normalization (shared continuum across all segments)

Main API:
    processed_spectra, processed_wavelengths = preprocess(
        raw_spectra, raw_wavelengths,
        wavelet_name='bior3.3', decomposition_level=None,
        sigma_threshold=3.0, denoise_method='mad', supercam_iterations=5,
        baseline_span=0.1, baseline_max_iter=5, baseline_b=3.5, baseline_tol=1e-3,
        return_continuum=False
    )
"""

import numpy as np
import pywt
import os
import csv

def guardar_resultados_csv(nombre_archivo, datos, encabezado=None):
    carpeta_destino = os.path.dirname(nombre_archivo)
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        if encabezado:
            writer.writerow(encabezado)
        writer.writerows(datos)

# --------------------------------------
# MAIN API
# --------------------------------------
def apply_preprocessing(raw_spectra,raw_wavelengths,
    wavelet_name='bior3.3', decomposition_level=None, sigma_threshold=3.0, denoise_method='mad', supercam_iterations=5,
    baseline_span=0.1, baseline_max_iter=5, baseline_b=3.5, baseline_tol=1e-3,
    return_continuum=False):
    """
    Preprocess raw spectral segments in groups of four.

    Steps:
      1) Denoise
      2) Stitch 
      3) Subtract baseline
      4) Trim each UV1,UV2,VIS,NIR group
      5) Normalize by shared continuum

    Returns:
      processed_spectra, processed_wavelengths (, continua)
    """
    # 1) Denoise
    denoised = denoise_spectra(raw_spectra, 
                                   wavelet_name = wavelet_name ,decomposition_level= decomposition_level,sigma_threshold = sigma_threshold,denoise_method = denoise_method,supercam_iterations = supercam_iterations)
    #2) Stitch
    stiched =  stitch_spectra(denoised, raw_wavelengths)
    #3) Subtract baseline
    corrected, continua = subtract_baseline(stiched, span=baseline_span, max_iter=baseline_max_iter, b=baseline_b, tol=baseline_tol)
    #4) Trim
    trimmed, trimmed_wavelengths = trim_overlap_regions(corrected, raw_wavelengths)
    #5) Normalize by shared continuum
    normalized, cont = normalize_by_continuum(continua, trimmed)

    wls = np.concatenate(trimmed_wavelengths)
    return (wls, normalized, cont) if return_continuum else (wls, normalized)

# --------------------------------------
# 1) DENOISING: undecimated wavelet + sigma clipping
# --------------------------------------
def denoise_spectra(
    spectra,
    wavelet_name='bior3.3',
    decomposition_level=None,
    sigma_threshold=3.0,
    denoise_method='mad',
    supercam_iterations=5
):    
    """
    Denoise a list of spectra using an undecimated wavelet transform
    and sigma-clipping on detail coefficients.

    Parameters:
        spectra : list of 1D numpy arrays
        wavelet_name : str
        decomposition_level : int or None
        sigma_threshold : float
        denoise_method : {'mad','supercam'}
        supercam_iterations : int

    Returns:
        denoised : list of 1D numpy arrays
    """
    def pad_to_multiple(x, base):
        rem = len(x) % base
        if rem == 0:
            return x, 0
        pad = base - rem
        return np.pad(x, (0, pad), mode='edge'), pad

    def sigma_clipping(coeffs, n_iter, sigma_thresh):
        filtered = []
        for cA, cD in coeffs:
            cD_abs = np.abs(cD)
            mask = np.ones_like(cD_abs, dtype=bool)
            for _ in range(n_iter):
                sigma = np.std(cD_abs[mask])
                mask = cD_abs < sigma_thresh * sigma
            final_sigma = np.std(cD_abs[mask])
            thr = sigma_thresh * final_sigma
            cD_filt = np.where(cD_abs < thr, 0, cD)
            filtered.append((cA, cD_filt))
        return filtered

    denoised = []
    for spec in spectra:
        spec = np.asarray(spec)
        orig_len = len(spec)
        lvl = decomposition_level
        if lvl is None:
            if orig_len % 2 != 0:
                spec = np.pad(spec, (0,1), mode='edge')
                orig_len += 1
            lvl = pywt.swt_max_level(orig_len)
        spec_padded, _ = pad_to_multiple(spec, 2**lvl)
        coeffs = pywt.swt(spec_padded, wavelet_name, level=lvl)
        if denoise_method == 'mad':
            new_coeffs = []
            for cA, cD in coeffs:
                sigma = np.median(np.abs(cD)) / 0.6745
                cD_filt = np.where(
                    np.abs(cD) < sigma_threshold * sigma,
                    0,
                    cD
                )
                new_coeffs.append((cA, cD_filt))
        else:
            new_coeffs = sigma_clipping(
                coeffs,
                n_iter=supercam_iterations,
                sigma_thresh=sigma_threshold
            )
        rec = pywt.iswt(new_coeffs, wavelet_name)
        denoised.append(rec[:orig_len])
    return denoised

# --------------------------------------
# 2) STITCHING
# --------------------------------------
def stitch_spectra(spectra, wavelengths):
    """
    Realiza el 'stitching' de múltiples espectros ajustando sus intensidades en zonas de solapamiento.

    Parámetros:
    -----------
    spectra : list of np.ndarray
        Lista de espectros a unir.
    wavelengths : list of np.ndarray
        Lista de longitudes de onda correspondientes a cada espectro.

    Devuelve:
    ---------
    stitched_spectra : list of np.ndarray
        Lista de espectros corregidos con los coeficientes de stitching aplicados.
    """
    #Declaración de los intervalos de solapamiento
    i1 = (wavelengths[1][1], wavelengths[0][len(wavelengths[0])-1])
    i2 = (wavelengths[2][1], wavelengths[1][len(wavelengths[1])-1])
    i3 = (wavelengths[3][1], wavelengths[2][len(wavelengths[2])-1])
    #Aislamiento de los intervalos de solapamiento
    datos_UV1_fil1 = spectra[0][(wavelengths[0] >= i1[0]) & (wavelengths[0] <= i1[1])]
    datos_UV2_fil1 = spectra[1][(wavelengths[1] >= i1[0]) & (wavelengths[1] <= i1[1])]
    datos_UV2_fil2 = spectra[1][(wavelengths[1] >= i2[0]) & (wavelengths[1] <= i2[1])]
    datos_VIS_fil2 = spectra[2][(wavelengths[2] >= i2[0]) & (wavelengths[2] <= i2[1])]
    datos_VIS_fil3 = spectra[2][(wavelengths[2] >= i3[0]) & (wavelengths[2] <= i3[1])]
    datos_NIR_fil3 = spectra[3][(wavelengths[3] >= i3[0]) & (wavelengths[3] <= i3[1])]
    #Extracción de las medianas
    mediana_UV1_fil1 = np.median(datos_UV1_fil1)
    mediana_UV2_fil1 = np.median(datos_UV2_fil1)
    mediana_UV2_fil2 = np.median(datos_UV2_fil2)
    mediana_VIS_fil2 = np.median(datos_VIS_fil2)
    mediana_VIS_fil3 = np.median(datos_VIS_fil3)
    mediana_NIR_fil3 = np.median(datos_NIR_fil3)
    #Cálculo de los coeficientes
    coef1 = mediana_UV2_fil1/mediana_UV1_fil1
    coef2 = mediana_VIS_fil2/mediana_UV2_fil2
    coef3 = mediana_NIR_fil3/mediana_VIS_fil3
    #Aplicación de los coeficientes
    datos_UV1_corr = spectra[0]*coef3*coef2*coef1
    datos_UV2_corr = spectra[1]*coef3*coef2
    datos_VIS_corr = spectra[2]*coef3
    datos_NIR_corr = spectra[3]
    sitich_coefs = [datos_UV1_corr, datos_UV2_corr, datos_VIS_corr, datos_NIR_corr]

    return sitich_coefs

# --------------------------------------
# 3) BASELINE: robust local regression + Tukey weights
# --------------------------------------
def subtract_baseline(
    spectra,
    span=0.1,
    max_iter=5,
    b=3.5,
    tol=1e-3
):
    """
    Estimate and subtract baseline from list of spectra.

    Parameters:
      spectra: list of 1D arrays
      span: fraction window size
      max_iter: int
      b: Tukey constant
      tol: float
    Returns:
      corrected: list of arrays
      continua: list of baselines
    """
    def tricube(w):
        w=np.abs(w)
        return np.where(w<1,(1-w**3)**3,0)
    def tukey(r,b):
        w=np.ones_like(r)
        m=r>=0
        w[m]=(1-(r[m]/b)**2)**2
        w[r>=b]=0
        return w
    corrected, continua = [], []
    for spec in spectra:
        n=len(spec); x=np.arange(n)
        half=int(np.ceil(span*n/2))
        base=spec.astype(float)
        for i in range(n):
            lo,hi=max(0,i-half),min(n,i+half+1)
            xl,yl=x[lo:hi],spec[lo:hi]
            w=tricube((xl-i)/half)
            p=np.polyfit(xl,yl,1,w=w)
            base[i]=np.polyval(p,i)
        for _ in range(max_iter):
            res=spec-base
            sigma=np.median(np.abs(res))/0.6745 if n>0 else 0
            rstd=res/(sigma if sigma else 1)
            wrob=tukey(rstd,b)
            newb=base.copy()
            for i in range(n):
                lo,hi=max(0,i-half),min(n,i+half+1)
                xl,yl=x[lo:hi],spec[lo:hi]
                w=tricube((xl-i)/half)*wrob[lo:hi]
                if w.sum()>0:
                    p=np.polyfit(xl,yl,1,w=w)
                    newb[i]=np.polyval(p,i)
            if np.linalg.norm(newb-base)<tol: break
            base=newb
        corr=spec-base
        corr[corr<0]=0
        continua.append(base)
        corrected.append(corr)
    return corrected, continua

# --------------------------------------
# 4) Trimming
# --------------------------------------
def trim_overlap_regions(spectra, wavelengths):
    """
    Recorta los espectros para conservar solo las regiones óptimas por detector:
    - UV1 para el solapamiento UV1-UV2
    - VIS para el solapamiento UV2-VIS
    - NIR para el solapamiento VIS-NIR
    - Elimina valores por encima de 1000 nm

    Parámetros:
    -----------
    spectra : list of np.ndarray
        Lista de espectros UV1, UV2, VIS, NIR.
    wavelengths : list of np.ndarray
        Lista de longitudes de onda correspondientes.

    Devuelve:
    ---------
    spectra_trimmed : list of np.ndarray
        Espectros recortados.
    wavelengths_trimmed : list of np.ndarray
        Longitudes de onda recortadas.
    """

    # Obtener intervalos de solapamiento
    i1_min, i1_max = wavelengths[1][1], wavelengths[0][-1]
    i2_min, i2_max = wavelengths[2][1], wavelengths[1][-1]
    i3_min, i3_max = wavelengths[3][1], wavelengths[2][-1]

    espectro_uv1 = spectra[0]
    wl_uv1 = wavelengths[0]
    # UV2: quedarse solo con su parte no solapada
    mask_uv2 = (wavelengths[1] >= i1_max) & (wavelengths[1] <= i2_min) 
    espectro_uv2 = spectra[1][mask_uv2]
    wl_uv2 = wavelengths[1][mask_uv2]

    # VIS: quitar el solapamiento con NIR
    mask_vis = (wavelengths[2] <= i3_min)
    espectro_vis = spectra[2][mask_vis]
    wl_vis = wavelengths[2][mask_vis]

    # NIR: desde i3_min hasta 1000nm
    mask_nir = wavelengths[3] <= 1000
    espectro_nir = spectra[3][mask_nir]
    wl_nir = wavelengths[3][mask_nir]

    return [espectro_uv1, espectro_uv2, espectro_vis, espectro_nir], [wl_uv1, wl_uv2, wl_vis, wl_nir]


# --------------------------------------
# 5) NORMALIZATION by shared continuum sum
# --------------------------------------
def normalize_by_continuum(continua, spectra):
    """
    Normalize concatenated spectra by total continuum sum.

    Parameters:
      continua: list of arrays
      spectra: list of arrays
    Returns:
      normalized: 1D array
    """
    cont = np.concatenate(continua)
    spec = np.concatenate(spectra)
    total = cont.sum()
    if total==0:
        raise ValueError("Continuum sum is zero.")
    return spec/total, cont



def apply_preprocessing_and_save(raw_spectra,raw_wavelengths, nombre_archivo_salida,
    wavelet_name='bior3.3', decomposition_level=None, sigma_threshold=3.0, denoise_method='mad', supercam_iterations=5,
    baseline_span=0.1, baseline_max_iter=5, baseline_b=3.5, baseline_tol=1e-3,
    return_continuum=False):

    lambdas, preprocessed_spectra = apply_preprocessing(raw_spectra,raw_wavelengths,
    wavelet_name='bior3.3', decomposition_level=None, sigma_threshold=3.0, denoise_method='mad', supercam_iterations=5,
    baseline_span=0.1, baseline_max_iter=5, baseline_b=3.5, baseline_tol=1e-3,
    return_continuum=False)

    datos = list(zip(lambdas, preprocessed_spectra))

    guardar_resultados_csv(nombre_archivo_salida, datos)

    return lambdas, preprocessed_spectra