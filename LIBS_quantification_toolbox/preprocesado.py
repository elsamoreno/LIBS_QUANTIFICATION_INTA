#Import libraries
import numpy as np
import pywt
from scipy.signal import argrelextrema
from scipy.interpolate import CubicSpline

# --------------------------------------
# FUNCIÓN PRINCIPAL DE PREPROCESADO
# --------------------------------------
def apply_preprocessing(spectra, wavelengths, normalization='none',
                        trim=True,
                        wavelet='bior3.3',
                        denoise_level=None,
                        denoise_threshold_sigma=3,
                        denoise_method='mad',
                        n_iter_supercam=5,
                        rbe_span=0.1,
                        rbe_max_iter=5,
                        rbe_b=3.5,
                        return_continuum=False):
    """
    Aplica el preprocesado completo a una lista de espectros: denoising + stitching + baseline removal + trim.

    Parámetros:
    -----------
    spectra : list of np.ndarray
        Lista de espectros originales.
    wavelengths : list of np.ndarray
        Lista de longitudes de onda para cada espectro.
    normalization : 'suma', 'continuo' o 'none'
        Método de normalización a aplicar. 'suma' normaliza por la suma total, 'continuo' por el continuo estimado, 'none' no aplica normalización.
    trim : bool, opcional
        Si es True, recorta los espectros y longitudes de onda en función de regiones de solapamiento óptimas.

    Devuelve:
    ---------
    spectra_final : list of np.ndarray
        Lista de espectros procesados.
    continuum_list : list of np.ndarray (opcional)
        Lista de continuos estimados, si return_continuum=True.
    wavelengths : list of np.ndarray
        Lista de longitudes de onda (posiblemente recortadas).
    """

    def get_param(param, i):
        return param[i] if isinstance(param, (list, tuple, np.ndarray)) else param

    # Inicializar listas de salida
    spectra_denoised = []

    # Denoising
    for i, spectrum in enumerate(spectra):
        wl = get_param(wavelet, i)
        lvl = get_param(denoise_level, i)
        sig = get_param(denoise_threshold_sigma, i)
        method = get_param(denoise_method, i)
        nit = get_param(n_iter_supercam, i)

        spectrum_denoised = denoise_spectrum_uwt(spectrum,
                                                 wavelet_name=wl,
                                                 level=lvl,
                                                 threshold_sigma=sig,
                                                 method=method,
                                                 n_iter_supercam=nit)
        spectra_denoised.append(spectrum_denoised)

    # Aplicar stitching
    spectra_stitched = stitch_spectra(spectra_denoised, wavelengths)  

    # Recortar espectros si se solicita
    if trim:
        spectra_stitched, wavelengths = trim_overlap_regions(spectra_stitched, wavelengths) 

    # Baseline removal
    spectra_final = []
    continuum_list = []

    for i, spectrum in enumerate(spectra_stitched):
        span = get_param(rbe_span, i)
        it_rbe = get_param(rbe_max_iter, i)
        b_val = get_param(rbe_b, i) 

        continuum, spectrum_baseless = robust_baseline_estimation(spectrum,
                                                                  span=span,
                                                                  max_iter=it_rbe,
                                                                  b=b_val)

        spectra_final.append(spectrum_baseless)
        continuum_list.append(continuum)

    # Normalización
    if normalization == 'suma':
        spectra_final = [normalizar_por_suma(spectrum) for spectrum in spectra_final]
    elif normalization == 'continuo':
        spectra_final = [normalizar_por_continuo(continuum, spectrum) for spectrum, continuum in zip(spectra_final, continuum_list)]

    if return_continuum:
        return spectra_final, continuum_list, wavelengths
    else:
        return spectra_final, wavelengths

# --------------------------------------
# 1. Denoising por Wavelet (UWT + sigma clipping)
# --------------------------------------
def denoise_spectrum_uwt(spectrum, wavelet_name='bior3.3', level=None, threshold_sigma=3, method='mad', n_iter_supercam=5):
    """
    Aplica reducción de ruido (denoising) a un espectro usando UWT y sigma clipping.

    Parámetros:
    ------------
    spectrum : array_like
        Espectro 1D original (array de intensidades).
    wavelet_name : str, opcional
        Nombre del wavelet a utilizar. Por defecto 'bior3.3'.
    level : int, opcional
        Nivel de descomposición wavelet. Si no se especifica, se calcula automáticamente el máximo.
    threshold_sigma : float, opcional
        Umbral de sigma para eliminar coeficientes de detalle (por defecto 3σ).
    method : str, opcional
        Método de sigma clipping: 'mad' o 'supercam'.
    n_iter_supercam : int, opcional
        Número de iteraciones para el método supercam.

    Devuelve:
    ---------
    spectrum_denoised : np.ndarray
        Espectro reconstruido con el ruido eliminado.
    """

    def pad_to_multiple(x, base):
        remainder = len(x) % base
        if remainder == 0:
            return x, 0
        pad_size = base - remainder
        x_padded = np.pad(x, (0, pad_size), mode='edge')
        return x_padded, pad_size

    def sigma_clipping_supercam(coeffs, n_iter=5, threshold_sigma=3):
        filtered_coeffs = []
        for cA, cD in coeffs:
            cD_abs = np.abs(cD)
            mask = np.ones_like(cD_abs, dtype=bool)
            for _ in range(n_iter):
                sigma = np.std(cD_abs[mask])
                mask = cD_abs < (threshold_sigma * sigma)
            sigma_final = np.std(cD_abs[mask])
            threshold = threshold_sigma * sigma_final
            cD_filtered = np.where(cD_abs < threshold, 0, cD)
            filtered_coeffs.append((cA, cD_filtered))
        return filtered_coeffs

    spectrum = np.asarray(spectrum)
    original_len = len(spectrum)

    if level is None:
        # Asegurar que la longitud sea par (agregar padding si es impar)
        if original_len % 2 != 0:
            spectrum = np.pad(spectrum, (0, 1), mode='edge')  # duplica el último valor
            original_len += 1
        level = pywt.swt_max_level(original_len)

    spectrum_padded, pad_size = pad_to_multiple(spectrum, 2 ** level)
    coeffs = pywt.swt(spectrum_padded, wavelet_name, level=level)

    if method == 'mad':
        denoised_coeffs = []
        for cA, cD in coeffs:
            sigma = np.median(np.abs(cD)) / 0.6745
            cD_filtered = np.where(np.abs(cD) < threshold_sigma * sigma, 0, cD)
            denoised_coeffs.append((cA, cD_filtered))
    elif method == 'supercam':
        denoised_coeffs = sigma_clipping_supercam(coeffs, n_iter=n_iter_supercam, threshold_sigma=threshold_sigma)
    else:
        raise ValueError("El parámetro 'method' debe ser 'mad' o 'supercam'.")

    spectrum_denoised = pywt.iswt(denoised_coeffs, wavelet_name)
    return spectrum_denoised[:original_len]

# --------------------------------------
# 2. Eliminación del continuo (por defecto: Robust Baseline Estimation)
# --------------------------------------
def robust_baseline_estimation(spectrum, span=0.1, max_iter=5, b=3.5, tol=1e-3):
    """
    Estima la línea base de un espectro utilizando el algoritmo RBE.

    Parámetros:
    ------------
    spectrum : array_like
        Espectro 1D original (array de intensidades).
    span : float, opcional
        Proporción del total de puntos a utilizar en la regresión local. Por defecto 0.1 (10%).
    max_iter : int, opcional
        Número máximo de iteraciones para la convergencia. Por defecto 5.
    b : float, opcional
        Constante de ajuste para los pesos bi-square de Tukey. Por defecto 3.5.
    tol : float, opcional
        Tolerancia para la convergencia. Por defecto 1e-3.

    Devuelve:
    ---------
    baseline : np.ndarray
        Línea base calculada para el espectro.
    spectrum_corrected : np.ndarray
        Espectro corregido tras la eliminación de la línea base.
    """

    x = np.arange(len(spectrum))
    n = len(spectrum)
    half_window = int(np.ceil(span * n / 2))

    # Estimación inicial de la línea base usando LOWESS
    baseline = np.copy(spectrum)
    for i in range(n):
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        x_local = x[start:end]
        y_local = spectrum[start:end]
        weights = tricube_weight((x_local - x[i]) / half_window)
        p = np.polyfit(x_local, y_local, 1, w=weights)
        baseline[i] = np.polyval(p, x[i])

    # Iteraciones para la estimación robusta
    for iteration in range(max_iter):
        residuals = spectrum - baseline
        sigma = np.median(np.abs(residuals)) / 0.6745
        residuals_standardized = residuals / sigma
        weights_robust = tukey_biweight(residuals_standardized, b)
        baseline_new = np.copy(spectrum)
        for i in range(n):
            start = max(0, i - half_window)
            end = min(n, i + half_window + 1)
            x_local = x[start:end]
            y_local = spectrum[start:end]
            weights = tricube_weight((x_local - x[i]) / half_window) * weights_robust[start:end]
            if np.sum(weights) > 0:
                p = np.polyfit(x_local, y_local, 1, w=weights)
                baseline_new[i] = np.polyval(p, x[i])
            else:
                baseline_new[i] = baseline[i]
        # Comprobar convergencia
        if np.linalg.norm(baseline_new - baseline) < tol:
            break
        baseline = baseline_new

    

    # Corregir el espectro restando la línea base
    spectrum_corrected = spectrum - baseline
    spectrum_corrected[spectrum_corrected < 0] = 0
    return baseline, spectrum_corrected

def tricube_weight(x):
    """Función de peso tricúbico."""
    abs_x = np.abs(x)
    return np.where(abs_x < 1, (1 - abs_x**3)**3, 0)

def tukey_biweight(residuals, b=3.5):
    """Pesos bi-square de Tukey asimétricos."""
    weights = np.ones_like(residuals)
    mask = residuals >= 0
    weights[mask] = (1 - (residuals[mask] / b)**2)**2
    weights[residuals >= b] = 0
    return weights

# --------------------------------------
# 3. Stitching/Estandarización
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
# 4. Normalización
# --------------------------------------
def normalizar_por_suma(espectro):
    """
    Normaliza un espectro dividiendo cada valor entre la suma total del espectro.

    Parámetros:
    ------------
    espectro : array_like
        Espectro original (array 1D de intensidades).

    Devuelve:
    ---------
    espectro_normalizado : np.ndarray
        Espectro normalizado.
    """
    espectro = np.asarray(espectro)
    suma_total = np.sum(espectro)

    if suma_total == 0:
        raise ValueError("La suma del espectro es cero, no se puede normalizar.")

    espectro_normalizado = espectro / suma_total
    return espectro_normalizado
def normalizar_por_continuo(continuum, espectro):
    """
    Normaliza un espectro dividiendo cada valor entre la suma total del espectro.

    Parámetros:
    ------------
    espectro : array_like
        Espectro original (array 1D de intensidades).

    Devuelve:
    ---------
    espectro_normalizado : np.ndarray
        Espectro normalizado.
    """
    espectro = np.asarray(espectro)
    suma_total = np.sum(continuum)

    if suma_total == 0:
        raise ValueError("La suma del contínuo es cero, no se puede normalizar.")

    espectro_normalizado = espectro / suma_total
    return espectro_normalizado

# --------------------------------------
# 5. Recorte de regiones de solapamiento
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
