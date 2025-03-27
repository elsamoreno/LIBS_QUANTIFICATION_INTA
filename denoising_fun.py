import pywt
import numpy as np

def denoise_spectrum_uwt(spectrum, wavelet_name='bior3.3', level=None, threshold_sigma=3):
    """
    Aplica reducción de ruido (denoising) a un espectro usando UWT y sigma clipping.

    Parámetros:
    ------------
    spectrum : array_like
        Espectro 1D original (array de intensidades).
    wavelet_name : str, opcional
        Nombre del wavelet a utilizar. Por defecto 'bior3.3'.
    level : int, opcional
        Nivel de descomposición wavelet. Si no se especifica, se calcula automáticamente.
    threshold_sigma : float, opcional
        Umbral de sigma para eliminar coeficientes de detalle (por defecto 3σ).

    Devuelve:
    ---------
    spectrum_denoised : np.ndarray
        Espectro reconstruido con el ruido eliminado.
    """


    # Asegurar entrada como array NumPy
    spectrum = np.asarray(spectrum)
    original_len = len(spectrum)

    # Obtener nivel máximo si no se especifica
    if level is None:
        level = pywt.swt_max_level(original_len)

    # Hacer padding si es necesario
    def pad_to_multiple(x, base):
        remainder = len(x) % base
        if remainder == 0:
            return x, 0
        pad_size = base - remainder
        x_padded = np.pad(x, (0, pad_size), mode='edge')
        return x_padded, pad_size

    spectrum_padded, pad_size = pad_to_multiple(spectrum, 2 ** level)

    # Descomposición SWT
    coeffs = pywt.swt(spectrum_padded, wavelet_name, level=level)

    # Aplicar sigma clipping (MAD) a los coeficientes de detalle
    denoised_coeffs = []
    for cA, cD in coeffs:
        sigma = np.median(np.abs(cD)) / 0.6745
        cD_filtered = np.where(np.abs(cD) < threshold_sigma * sigma, 0, cD)
        denoised_coeffs.append((cA, cD_filtered))

    # Reconstrucción
    spectrum_denoised = pywt.iswt(denoised_coeffs, wavelet_name)
    return spectrum_denoised[:original_len]