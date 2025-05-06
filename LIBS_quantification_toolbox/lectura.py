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
    carpeta_destino = os.path.dirname(nombre_archivo)
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        if encabezado:
            writer.writerow(encabezado)
        writer.writerows(datos)


def cargar_espectros(carpeta, nombre_base, quitar_extremos=True):
    """
    Carga automáticamente los archivos UV1, UV2, VIS y NIR relacionados con un mismo espectro.

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



def cargar_espectros_5shots(carpeta, nombre_base, quitar_extremos=True, lb = False):
    """
    Carga automáticamente los archivos UV1, UV2, VIS y NIR correspondientes a los 5 shots de un mismo spot.

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
        Lista de espectros UV1, UV2, VIS, NIR correspondientes a cada shot (n1, n2, n3, n4 y n5).
    wavelengths : list of np.ndarray
        Lista de longitudes de onda correspondientes.
    nombres : list of str
        Lista de nombres de los espectros (UV1, UV2, VIS, NIR).
    """
    if  lb:
        nombre_base_n1 = f"{nombre_base}_n1"
        nombre_base_n2 = f"{nombre_base}_n2"
        nombre_base_n3 = f"{nombre_base}_n3"
        nombre_base_n4 = f"{nombre_base}_n4"
        nombre_base_n5 = f"{nombre_base}_n5"
    else:
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

    return wavelengths, espectros_n1, espectros_n2, espectros_n3, espectros_n4, espectros_n5, nombres


def cargar_espectros_5shotsprom(carpeta, nombre_base, quitar_extremos=True,lb = False, save = False):

    """
    Carga automáticamente los archivos UV1, UV2, VIS y NIR de los 5 shots realizados sobre un spot.
    El primer shot se descarta, así como los que tengan un nivel energético muy alto (estado de saturación)
    o muy bajo. Esta última característica se evalúa a través del espectro en el rango del visible.
    Los espectros de los shots restantes se promedian para obtener un espectro final.


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
    ws : list of np.ndarray
        Lista de longitudes de onda correspondientes.
    espectros : list of np.ndarray
        Lista de espectros UV1, UV2, VIS y NIR promediados
    nombres: list of str
        Lista de nombres de los espectros (UV1, UV2, VIS, NIR).
    """
        
    ws, n1, n2, n3, n4, n5, nombres = cargar_espectros_5shots(carpeta, nombre_base,lb = lb)

    partes = os.path.normpath(carpeta).split(os.sep)


    #umbral_saturacion = 0.99 * 65535  # Nivel de filtrado superior para evitar espectros saturados
    umbral_saturacion = 65000  # Nivel de filtrado superior para evitar espectros saturados
    #umbral_energia = 0.5 * 65535      # Nivel de filtrado inferior para evitar espectros poco energéticos

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
        #if umbral_energia < max_val < umbral_saturacion:
        if  max_val < umbral_saturacion:
            indices_validos.append(i)

    if len(indices_validos) == 0:
        print(f"No hay espectros validos para calcular la media en el shot {i}.")
        UV1_prom = None
        UV2_prom = None
        VIS_prom = None
        NIR_prom = None
        intensidades = None
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

        intensidades = [UV1_prom, UV2_prom, VIS_prom, NIR_prom]
        if save:
            try:
                idx_level0 = partes.index("Level0")
                mx = partes[idx_level0 + 1]
                py = partes[idx_level0 + 2]
            except (ValueError, IndexError):
                raise ValueError(f"No se pudo extraer MX y PY desde la ruta: {carpeta}")
            # Guardar los resultados en un archivo CSV
            # Crear la carpeta de salida si no existe
            if not os.path.exists("../Spectra/FinalSamplesTrial/Level1"):
                os.makedirs("../Spectra/FinalSamplesTrial/Level1")
                # Construir la ruta de salida
                nombre_archivo_salida = f"../Spectra/FinalSamplesTrial/Level1/LV1_{mx}_{py}.txt"
                datos = [] 
                for lmbs, ints in zip(ws, intensidades):
                    for l, i in zip(lmbs, ints):
                        datos.append([l, i])
                
                # Guardar datos de nivel 1
                guardar_resultados_csv(nombre_archivo_salida, datos)
    return ws, intensidades, nombres


def cargar_espectros_5shotspromV2_0(carpeta, nombre_base, quitar_extremos=True):
    """
    Carga automáticamente los archivos UV1, UV2, VIS y NIR de los 5 shots realizados sobre un spot.
    El primer shot se descarta, así como los que tengan un nivel energético muy alto (estado de saturación)
    o muy bajo. Esta última característica se evalúa a través del espectro en el rango del visible.
    Los espectros de los shots restantes se promedian para obtener un espectro final.

    Parámetros:
    -----------
    carpeta : str
        Nombre de la subcarpeta dentro de '../Spectra/'.
    nombre_base : str
        ***Este parámetro ya no se usa para construir los nombres de archivo.***
    quitar_extremos : bool, opcional
        Si True, elimina los primeros y últimos 16 valores (por defecto True).

    Devuelve:
    ---------
    ws : list of np.ndarray
        Lista de longitudes de onda correspondientes.
    espectros : list of np.ndarray
        Lista de espectros UV1, UV2, VIS y NIR promediados
    nombres: list of str
        Lista de nombres de los espectros (UV1, UV2, VIS, NIR).
    """

    partes = os.path.normpath(carpeta).split(os.sep)

    try:
        idx_level0 = partes.index("Level0")
        mx = partes[idx_level0 + 1]
        py = partes[idx_level0 + 2]
    except (ValueError, IndexError):
        raise ValueError(f"No se pudo extraer MX y PY desde la ruta: {carpeta}")

    # Nuevo nombre base automático
    base = f"{mx}_{py}_shot"

    # Cargar datos manualmente con nombres construidos
    espectros_shots = []
    nombres = ["UV1", "UV2", "VIS", "NIR"]
    ws = []

    for shot in range(1, 6):
        espectros_por_cod = []
        longitudes = []

        for cod in nombres:
            archivo = os.path.join("../Spectra", carpeta, f"{base}{shot}_{cod}.xy")
            try:
                data = np.loadtxt(archivo)
                if quitar_extremos:
                    longitudes.append(data[16:-16, 0])
                    espectros_por_cod.append(data[16:-16, 1])
                else:
                    longitudes.append(data[:, 0])
                    espectros_por_cod.append(data[:, 1])
            except Exception as e:
                raise FileNotFoundError(f"No se pudo cargar el archivo: {archivo}\n{e}")

        if not ws:
            ws = longitudes
        espectros_shots.append(espectros_por_cod)

    espectros_shots = np.array(espectros_shots)  # Shape: (5 shots, 4 rangos, N puntos)

    umbral_saturacion = 0.95 * 65535
    umbral_energia = 0.5 * 65535

    indices_validos = []
    for i, spec_vis in enumerate(espectros_shots[:, 2]):  # VIS en índice 2
        max_val = np.max(spec_vis)
        if umbral_energia < max_val < umbral_saturacion:
            indices_validos.append(i)

    if len(indices_validos) == 0:
        print(f"No hay espectros válidos para calcular la media en el spot {mx}_{py}.")
        intensidades = [None] * 4
    else:
        intensidades = []
        for j in range(4):  # Para UV1, UV2, VIS, NIR
            promedio = np.mean([espectros_shots[i][j] for i in indices_validos], axis=0)
            intensidades.append(promedio)

        # Guardar espectros promedio
        nombre_archivo_salida = f"../Spectra/FinalSamplesTrial/Level1/LV1_{mx}_{py}.txt"
        datos = []
        for lmbs, ints in zip(ws, intensidades):
            for l, i in zip(lmbs, ints):
                datos.append([l, i])
        guardar_resultados_csv(nombre_archivo_salida, datos)

    return ws, intensidades, nombres
