import matplotlib.pyplot as plt
import numpy as np

def plot_spectra(wavelengths, espectros, titulo, nombres=None, 
                 xlabel="Longitud de onda (nm)", ylabel="Intensidad (cuentas)", figsize=(12, 5)):
    """
    Representa múltiples espectros en una misma gráfica.

    Parámetros:
    -----------
    wavelengths : list of np.ndarray
        Lista de longitudes de onda para cada espectro.
    espectros : list of np.ndarray
        Lista de espectros (intensidades) a representar.
    nombres : list of str, opcional
        Etiquetas para cada espectro. Si no se proporciona, se enumeran como 'Espectro 1', 'Espectro 2', ...
    titulo : str, opcional
        Título de la gráfica.
    xlabel : str, opcional
        Etiqueta del eje X.
    ylabel : str, opcional
        Etiqueta del eje Y.
    figsize : tuple, opcional
        Tamaño de la figura (por defecto (12, 5)).
    """

    if nombres is None:
        nombres = [f"Shot {i+1}" for i in range(len(espectros))]

    plt.figure(figsize=figsize)
    

    for i in range(len(espectros)):
        if wavelengths[i] is not None and espectros[i] is not None:
            plt.plot(wavelengths[i], espectros[i], label=nombres[i])
        else:
            print(f"Aviso: El espectro {i} o su longitud de onda es None y no se representará.")

    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


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


