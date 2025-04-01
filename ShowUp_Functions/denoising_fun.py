import pywt
import numpy as np

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