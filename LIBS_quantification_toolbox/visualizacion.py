import matplotlib.pyplot as plt

def plot_spectra(wavelengths, espectros, nombres=None, titulo="Espectros", 
                 xlabel="Longitud de onda (nm)", ylabel="Intensidad", figsize=(12, 5)):
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
        nombres = [f"Espectro {i+1}" for i in range(len(espectros))]

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
