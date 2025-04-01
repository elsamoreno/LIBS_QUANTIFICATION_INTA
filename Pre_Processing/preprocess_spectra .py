#Import libraries
import numpy as np
import pywt
from scipy.signal import argrelextrema
from scipy.interpolate import CubicSpline
from denoising_fun import  denoise_spectrum_uwt

# --------------------------------------
# FUNCIÓN PRINCIPAL DE PREPROCESADO
# --------------------------------------
def preprocesar_espectro(spectrum,
                         wavelet='bior3.3',
                         denoise_level=None,
                         denoise_threshold_sigma = 3,
                         denoise_method='mad',
                         n_iter_supercam=5,
                         rbe_span=0.1,
                         rbe_max_iter=5,
                         rbe_b=3.5,
                         normalization='suma',
                         return_continuum=False):
    """
    Aplica el preprocesado completo: denoising + baseline removal + normalización.

    Parámetros:
    -----------
    spectrum : array_like
        Espectro original.
    wavelet : str
        Nombre del wavelet para el denoising.
    denoise_level : int o None
        Nivel de descomposición del wavelet.
    denoise_threshold_sigma : float
        Umbral para sigma clipping.
    denoise_method : 'mad' o 'supercam'
        Método de sigma clipping.
    n_iter_supercam : int
        Número de iteraciones para sigma clipping tipo SuperCam.
    rbe_span : float
        Proporción de puntos usados en la regresión local robusta.
    rbe_max_iter : int
        Número máximo de iteraciones para RBE.
    rbe_b : float
        Constante para la función bi-square en RBE.
    normalization : 'suma' o 'continuo'
        Método para realizar el sigma Clipping.
    return_continuum : bool
        Si True, también devuelve el continuo estimado.

    Devuelve:
    ---------
    spectrum_final : np.ndarray
        Espectro corregido, limpio y normalizado.
    continuum : np.ndarray (opcional)
        Continuo estimado (si return_continuum=True).
    """

    # 1. Denoising
    spectrum_denoised = denoise_spectrum_uwt(spectrum, wavelet=wavelet,
                                             level=denoise_level,
                                             threshold_sigma=denoise_threshold_sigma,
                                             method=denoise_method,
                                             n_iter_supercam=n_iter_supercam)                                            

    # 2. Baseline removal
    spectrum_baseless, continuum = robust_baseline_estimation(spectrum_denoised,
                                                              span=rbe_span, 
                                                              max_iter=rbe_max_iter, 
                                                              b=rbe_b)

    # 3. Normalización
    if normalization == 'suma':
        spectrum_final = normalizar_por_suma(spectrum_baseless)
    elif normalization == 'continuo':
        spectrum_final = normalizar_por_continuo(continuum, spectrum_baseless)
    else:
        raise ValueError("Método de normalización no reconocido: usa 'suma' o 'continuo'.")

    if return_continuum:
        return spectrum_final, continuum
    else:
        return spectrum_final


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
# 3. Normalización
# --------------------------------------
# Normalización por suma
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

# Normalización por continuo
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


