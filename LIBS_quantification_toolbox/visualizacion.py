import matplotlib.pyplot as plt
import numpy as np


def plot_spectra(wavelengths, espectros, titulo, nombres=None, 
                 xlabel="Longitud de onda (nm)", 
                 ylabel="Intensidad (cuentas)", 
                 figsize=(12, 5)):
    """
    Plot one or more spectra (wavelength vs. intensity) on the same axes.

    Parameters
    ----------
    wavelengths : array_like or list of array_like
        Wavelength axis (nm) for each spectrum, either a single 1D array or
        a list of 1D arrays or lists of arrays (for multi-range spectra).
    espectros : array_like or list of array_like
        Intensity axis for each spectrum, matching lengths/shapes of
        `wavelengths`.
    title : str
        Figure title.
    nombres : list of str, optional
        Legend labels for each spectrum.
    xlabel : str, optional
        X-axis label.
    ylabel : str, optional
        Y-axis label.
    figsize : tuple, optional
        Matplotlib figure size.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created Figure object.
    ax : matplotlib.axes.Axes
        The Axes with the plotted spectra.
    """
    # --- Wrap single-spectrum inputs into lists ---
    if isinstance(wavelengths, np.ndarray) and isinstance(espectros, np.ndarray):
        wavelengths = [wavelengths]
        espectros = [espectros]

    # --- Convert any tuples to lists for uniformity ---
    wavelengths = list(wavelengths)
    espectros = list(espectros)

    # --- Basic validation ---
    if len(wavelengths) != len(espectros):
        raise ValueError(f"Number of wavelength arrays ({len(wavelengths)}) "
                         f"!= number of intensity arrays ({len(espectros)})")

    # --- Prepare labels ---
    n = len(espectros)
    if nombres is None:
        nombres = [f"Shot {i+1}" for i in range(n)]
    if len(nombres) != n:
        raise ValueError(f"Length of labels ({len(nombres)}) != number of spectra ({n})")

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=figsize)

    for wl_entry, sp_entry, lbl in zip(wavelengths, espectros, nombres):
        # Caso 1: espectro simple (una sola medición)
        if isinstance(wl_entry, np.ndarray) and wl_entry.ndim == 1:
            ax.plot(wl_entry, sp_entry, label=lbl)
        else:
            # Caso 2: múltiples bloques (p. ej., 4 espectrómetros)
            wl_blocks = [np.asarray(b) for b in wl_entry]
            sp_blocks = [np.asarray(b) for b in sp_entry]

            if len(wl_blocks) != len(sp_blocks):
                raise ValueError(f"Number of blocks mismatch in '{lbl}'")

            # Concatenar con np.nan para evitar líneas entre bloques
            merged_wl = []
            merged_sp = []
            for wl_block, sp_block in zip(wl_blocks, sp_blocks):
                if wl_block.shape != sp_block.shape:
                    raise ValueError(f"Shape mismatch in '{lbl}': {wl_block.shape} vs {sp_block.shape}")
                merged_wl.extend(wl_block.tolist() + [np.nan])
                merged_sp.extend(sp_block.tolist() + [np.nan])

            merged_wl = np.array(merged_wl)
            merged_sp = np.array(merged_sp)
            ax.plot(merged_wl, merged_sp, label=lbl)

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
    plt.show()

    return fig, ax




def plot_and_save_spectra(wavelengths, espectros, titulo, archivo_salida, nombres=None, 
                          xlabel="Longitud de onda (nm)", 
                          ylabel="Intensidad (cuentas)", 
                          figsize=(12, 5), formato="png"):
    """
    Plot one or more spectra (wavelength vs. intensity) on the same axes,
    and save the plot to a file.

    Parameters
    ----------
    wavelengths : array_like or list of array_like
        Wavelength axis (nm) for each spectrum, either a single 1D array or
        a list of 1D arrays or lists of arrays (for multi-range spectra).
    espectros : array_like or list of array_like
        Intensity axis for each spectrum, matching lengths/shapes of
        `wavelengths`.
    titulo : str
        Figure title.
    archivo_salida : str
        File path to save the plot (e.g., "plot.png").
    nombres : list of str, optional
        Legend labels for each spectrum.
    xlabel : str, optional
        X-axis label.
    ylabel : str, optional
        Y-axis label.
    figsize : tuple, optional
        Matplotlib figure size.
    formato : str, optional
        Format of the saved plot, default is "png".

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created Figure object.
    ax : matplotlib.axes.Axes
        The Axes with the plotted spectra.
    """
    # --- Wrap single-spectrum inputs into lists ---
    if isinstance(wavelengths, np.ndarray) and isinstance(espectros, np.ndarray):
        wavelengths = [wavelengths]
        espectros = [espectros]

    # --- Convert any tuples to lists for uniformity ---
    wavelengths = list(wavelengths)
    espectros = list(espectros)

    # --- Basic validation ---
    if len(wavelengths) != len(espectros):
        raise ValueError(f"Number of wavelength arrays ({len(wavelengths)}) "
                         f"!= number of intensity arrays ({len(espectros)})")

    # --- Prepare labels ---
    n = len(espectros)
    if nombres is None:
        nombres = [f"Shot {i+1}" for i in range(n)]
    if len(nombres) != n:
        raise ValueError(f"Length of labels ({len(nombres)}) != number of spectra ({n})")

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=figsize)

    for wl_entry, sp_entry, lbl in zip(wavelengths, espectros, nombres):
        # Caso 1: espectro simple (una sola medición)
        if isinstance(wl_entry, np.ndarray) and wl_entry.ndim == 1:
            ax.plot(wl_entry, sp_entry, label=lbl)
        else:
            # Caso 2: múltiples bloques (p. ej., 4 espectrómetros)
            wl_blocks = [np.asarray(b) for b in wl_entry]
            sp_blocks = [np.asarray(b) for b in sp_entry]

            if len(wl_blocks) != len(sp_blocks):
                raise ValueError(f"Number of blocks mismatch in '{lbl}'")

            # Concatenar con np.nan para evitar líneas entre bloques
            merged_wl = []
            merged_sp = []
            for wl_block, sp_block in zip(wl_blocks, sp_blocks):
                if wl_block.shape != sp_block.shape:
                    raise ValueError(f"Shape mismatch in '{lbl}': {wl_block.shape} vs {sp_block.shape}")
                merged_wl.extend(wl_block.tolist() + [np.nan])
                merged_sp.extend(sp_block.tolist() + [np.nan])

            merged_wl = np.array(merged_wl)
            merged_sp = np.array(merged_sp)
            ax.plot(merged_wl, merged_sp, label=lbl)

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()

    # Guardar la gráfica
    fig.savefig(archivo_salida, format=formato)

    # Mostrar la gráfica
    plt.show()

    return fig, ax
