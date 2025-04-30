import matplotlib.pyplot as plt
import numpy as np

def plot_spectra(wavelengths, espectros, titulo, nombres=None, 
                 xlabel="Longitud de onda (nm)", 
                 ylabel="Intensidad (cuentas)", 
                 figsize=(12, 5)):
    """
    Plot one or more spectra (wavelength vs. intensity) on the same axes.

    This function accepts either:
      1. Single-spectrum inputs:
         - `wavelengths`: 1D array of length N
         - `intensities`: 1D array of length N
      2. Multi-spectrum inputs:
         - `wavelengths`: list/tuple of M arrays [wl_1, wl_2, ..., wl_M]
         - `intensities`: list/tuple of M arrays [sp_1, sp_2, ..., sp_M]
    Parameters
    ----------
    wavelengths : array_like or list of array_like
        Wavelength axis (nm) for each spectrum, either a single 1D array or
        a list of 1D arrays.
    espectros : array_like or list of array_like
        Intensity axis for each spectrum, matching lengths/shapes of
        `wavelengths`.
    title : str
        Figure title.
    nombres : list of str, optional
        Legend labels for each spectrum. If omitted, spectra are labeled
        "Spec 1", "Spec 2", ...
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
    for wl, sp, lbl in zip(wavelengths, espectros, nombres):
        wl = np.asarray(wl)
        sp = np.asarray(sp)
        if wl.shape != sp.shape:
            raise ValueError(f"Shape mismatch: wavelengths {wl.shape} vs intensities {sp.shape}")
        ax.plot(wl, sp, label=lbl)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
    plt.show()

    return fig, ax



def plot_multiple_spectra_vertical(wavelengths, espectros, titulo, nombres=None, xlabel="Longitud de onda (nm)", ylabel="Intensidad (cuentas)"):
    if nombres is None:
        nombres = [f"Espectro {i+1}" for i in range(len(espectros))]

    num_spectra = len(espectros)
    fig, axs = plt.subplots(num_spectra, 1, figsize=(8, 3 * num_spectra), sharex=True)

    if num_spectra == 1:
        axs = [axs]  # Asegurar que axs siempre sea una lista

    # Primer plot: cada espectro en su subplot
    for i in range(num_spectra):
        if wavelengths[i] is not None and espectros[i] is not None:
            # Convertir a arrays 1D, asegurando que no haya listas anidadas
            w = np.concatenate(wavelengths[i]) if isinstance(wavelengths[i][0], (list, np.ndarray)) else np.array(wavelengths[i])
            e = np.concatenate(espectros[i]) if isinstance(espectros[i][0], (list, np.ndarray)) else np.array(espectros[i])

            w = w.flatten()
            e = e.flatten()

            axs[i].plot(w, e, label=nombres[i])
            axs[i].set_xlabel(xlabel)
            axs[i].set_ylabel(ylabel)
            axs[i].set_title(f"{nombres[i]} - {titulo}")
            axs[i].grid(True)
            axs[i].legend()
        else:
            print(f"Aviso: El espectro {i} o su longitud de onda es None y no se representará.")

    fig.tight_layout()
    plt.show()

    # Segundo plot: superponer todos los espectros
    fig2, ax2 = plt.subplots(figsize=(8, 6))

    for i in range(num_spectra):
        if wavelengths[i] is not None and espectros[i] is not None:
            w = np.concatenate(wavelengths[i]) if isinstance(wavelengths[i][0], (list, np.ndarray)) else np.array(wavelengths[i])
            e = np.concatenate(espectros[i]) if isinstance(espectros[i][0], (list, np.ndarray)) else np.array(espectros[i])

            w = w.flatten()
            e = e.flatten()

            ax2.plot(w, e, label=nombres[i])
        else:
            continue

    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    ax2.set_title(f"Superposición de espectros - {titulo}")
    ax2.grid(True)
    ax2.legend()
    fig2.tight_layout()
    plt.show()


