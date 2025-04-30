import os
import pandas as pd
import numpy as np
import csv

def leer_archivo_txt(nombre_archivo, saltar_lineas=5, delimitador=';'):
    try:
        df = pd.read_csv(nombre_archivo, delimiter=delimitador, skiprows=saltar_lineas)
        df.columns = df.columns.str.strip()
        df['Wave'] = pd.to_numeric(df['Wave'], errors='coerce')
        df['Sample'] = pd.to_numeric(df['Sample'], errors='coerce')
        df.dropna(inplace=True)

        espectro = df['Sample'].values
        wavelength = df['Wave'].values
        return espectro, wavelength
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None
    
def guardar_resultados_csv(nombre_archivo, datos, encabezado=None):
    # Asegurarnos de que la carpeta existe
    carpeta_destino = os.path.dirname(nombre_archivo)
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)  # Crea la carpeta si no existe

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        if encabezado:
            writer.writerow(encabezado)  # Escribe la cabecera si se proporciona
        writer.writerows(datos)  # Escribe las filas de datos

def cargar_espectros(carpeta, nombre_base, quitar_extremos=True):
    """
    Carga automáticamente los archivos UV1, UV2, VIS y NIR relacionados con un mismo experimento.

    Parámetros:
    -----------
    carpeta : str
        Nombre de la subcarpeta dentro de '../Spectra/'.
    nombre_base : str
        Parte común del nombre del archivo sin el sufijo numérico.
    quitar_extremos : bool, opcional
        Si True, elimina los primeros y últimos 16 valores (por defecto True).

    Devuelve:
    ---------
    espectros : list of np.ndarray
        Lista de espectros UV1, UV2, VIS, NIR.
    wavelengths : list of np.ndarray
        Lista de longitudes de onda correspondientes.
    nombres : list of str
        Lista de nombres de los espectros (UV1, UV2, VIS, NIR).
    """
    
    codigos = ['7324767SP', '7324768SP', '7324769SP', '7324770SP']
    nombres = ['UV1', 'UV2', 'VIS', 'NIR']
    espectros = []
    wavelengths = []

    for codigo in codigos:
        ruta = os.path.join('..', 'Spectra', carpeta, f"{nombre_base}_{codigo}.txt")
        espectro, wave = leer_archivo_txt(ruta)

        if espectro is None or wave is None:
            print(f"No se pudo cargar el archivo: {ruta}")
            espectros.append(None)
            wavelengths.append(None)
            continue

        if quitar_extremos:
            espectro = espectro[16:-16]
            wave = wave[16:-16]

        espectros.append(espectro)
        wavelengths.append(wave)

    return espectros, wavelengths, nombres



def cargar_espectros_5shots(carpeta, nombre_base, quitar_extremos=True):
    nombre_base_n1 = f"{nombre_base}-n1"
    nombre_base_n2 = f"{nombre_base}-n2"
    nombre_base_n3 = f"{nombre_base}-n3"
    nombre_base_n4 = f"{nombre_base}-n4"
    nombre_base_n5 = f"{nombre_base}-n5"
    espectros_n1, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n1)
    espectros_n2, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n2)
    espectros_n3, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n3)
    espectros_n4, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n4)
    espectros_n5, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n5)

    return nombres, wavelengths, espectros_n1, espectros_n2, espectros_n3, espectros_n4, espectros_n5


def cargar_espectros_5shotsprom(carpeta, nombre_base, quitar_extremos=True):
    n, ws, n1, n2, n3, n4, n5 = cargar_espectros_5shots(carpeta, nombre_base)

    umbral_saturacion = 0.95 * 65535  # Nivel de filtrado superior para evitar espectros saturados
    umbral_energia = 0.5 * 65535      # Nivel de filtrado inferior para evitar espectros poco energéticos

    # Agrupamos los espectros en función del rango de frecuencias descartando el primer shot
    espectros_UV1 = np.array([n1[0], n2[0], n3[0], n4[0], n5[0]])
    espectros_UV2 = np.array([n1[1], n2[1], n3[1], n4[1], n5[1]])
    espectros_VIS = np.array([n1[2], n2[2], n3[2], n4[2], n5[2]])
    espectros_NIR = np.array([n1[3], n2[3], n3[3], n4[3], n5[3]])

    # Índices de los shots válidos según el VIS
    indices_validos = []

    # Filtramos los espectros para deshacernos de los saturados o muy poco energéticos
    for i, spec_vis in enumerate(espectros_VIS):
        max_val = np.max(spec_vis)
        if umbral_energia < max_val < umbral_saturacion:
            indices_validos.append(i)

    if len(indices_validos) == 0:
        print(f"No hay espectros validos para calcular la media en el shot {i}.")
        UV1_prom = None
        UV2_prom = None
        VIS_prom = None
        NIR_prom = None
    else:
        # Filtramos todos los arrays con los índices válidos
        UV1_filtrado = [espectros_UV1[i] for i in indices_validos]
        UV2_filtrado = [espectros_UV2[i] for i in indices_validos]
        VIS_filtrado = [espectros_VIS[i] for i in indices_validos]
        NIR_filtrado = [espectros_NIR[i] for i in indices_validos]

        UV1_prom = np.mean(UV1_filtrado, axis=0)
        UV2_prom = np.mean(UV2_filtrado, axis=0)
        VIS_prom = np.mean(VIS_filtrado, axis=0)
        NIR_prom = np.mean(NIR_filtrado, axis=0)

        ruta = f"{carpeta}"/../Level1"
        nombre_archivo = os.path.join(ruta, "LV1_M1_P1")

        resultados = list(zip(UV1_prom, UV2_prom, VIS_prom, NIR_prom))  # Combinamos las listas
        encabezado = ['UV1', 'UV2', 'VIS', 'NIR']
        guardar_resultados_csv(nombre_archivo, resultados, encabezado)

    return n, ws, UV1_prom, UV2_prom, VIS_prom, NIR_prom



