import os
import pandas as pd
import numpy as np
import csv



def leer_archivo_txt(nombre_archivo, saltar_lineas=5, delimitador=';',dark=False):
    if dark:
        try:
            df = pd.read_csv(nombre_archivo, delimiter=delimitador, skiprows=saltar_lineas)
            df.columns = df.columns.str.strip()
            df['Dark'] = pd.to_numeric(df['Dark'], errors='coerce')
            df.dropna(inplace=True)

            dark = df['Dark'].values
            return dark, 0
        except Exception as e:
            print(f"Error al leer el Dark: {e}")
            return None, None
    else:
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


def cargar_espectros(carpeta, nombre_base, quitar_extremos=True, dark=False):
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
    dark : bool, opcional
        Si True, carga el dark (por defecto False).

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

    if dark:
        #Sacamos el dark del primer espectro
        dark_path = os.path.join('..', 'Spectra', carpeta, f"{nombre_base}_7324767SP.txt")
        dark, _ = leer_archivo_txt(dark_path, dark=True)
        return espectros, wavelengths, nombres, dark
    else:
        return espectros, wavelengths, nombres



def cargar_espectros_5shots(carpeta, nombre_base, quitar_extremos=True, lb = False):
    """
    Carga automáticamente los archivos UV1, UV2, VIS, NIR y Dark correspondientes a los 5 shots de un mismo spot.

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
    #Sacamos el dark del primer espectro
    espectros_n1, wavelengths, nombres, dark = cargar_espectros(carpeta, nombre_base_n1, dark=True)
    espectros_n2, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n2)
    espectros_n3, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n3)
    espectros_n4, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n4)
    espectros_n5, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n5)

    return wavelengths, espectros_n1, espectros_n2, espectros_n3, espectros_n4, espectros_n5, dark, nombres


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

# TODO: Cambiar esta función para que coja los archivos de manera 'MY_PZ_shotX_UV1'
def cargar_espectros_5shots(carpeta, nombre_base, quitar_extremos=True, lb = False):
    """
    Carga automáticamente los archivos UV1, UV2, VIS, NIR y Dark correspondientes a los 5 shots de un mismo spot.

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
    #Sacamos el dark del primer espectro
    espectros_n1, wavelengths, nombres, dark = cargar_espectros(carpeta, nombre_base_n1, dark=True)
    espectros_n2, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n2)
    espectros_n3, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n3)
    espectros_n4, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n4)
    espectros_n5, wavelengths, nombres = cargar_espectros(carpeta, nombre_base_n5)

    return wavelengths, espectros_n1, espectros_n2, espectros_n3, espectros_n4, espectros_n5, dark, nombres


def cargar_espectros_5shotspromV2_0(carpeta, nombre_base, lb = False):
    """
    Carga y promedia los 5 shots de un spot, descartando:
      - El primer shot
      - Cualquier shot cuya intensidad máxima supere un umbral de saturación
        , en **cualquiera** de las bandas
      - Resta el dark correspondiente a cada shot válido
      - (Opcional) Recorta 16 puntos al inicio y final de cada espectro

    Parámetros
    ----------
    carpeta : str
        Subcarpeta dentro de '../Spectra/'.
    nombre_base : str
        Nombre común de los archivos sin sufijo numérico.
    lb : bool
        Si True usa sufijos '_nX', si False '-nX'.
    quitar_extremos : bool
        Si True elimina los 16 primeros y últimos puntos de cada espectro.

    Devuelve
    -------
    ws : list[np.ndarray]
        Lista de 4 arrays de longitudes de onda (UV1, UV2, VIS, NIR).
    intensidades : list[np.ndarray] or None
        Lista de 4 arrays con los espectros promedio de los shots válidos,
        o None si no hubo shots válidos.
    nombres : list[str]
        ['UV1','UV2','VIS','NIR']
    """
    # 1) Cargo los 5 shots + dark
    ws, n1, n2, n3, n4, n5,drk, nombres = cargar_espectros_5shots(carpeta, nombre_base, lb = lb)

    # 2) Agrupo por banda y descarto el primer shot (índice 0)
    drk_arr = np.stack(drk, axis=0)  # (4 bandas, N pixels)
    shots = np.stack([n1, n2, n3, n4, n5], axis=0)  # (5,4,N)
    shots = shots[1:, ...]  # (4,4,N)

    # 3) Filtro por saturación/nivel bajo en todas las bandas
    umbral_max = 65000
    umbral_min =    0  # ajustable
    valid_idxs = []
    for i in range(shots.shape[0]):
        # intensidades máximas por banda en el shot i
        max_per_band = shots[i].max(axis=1)  # (4,)
        if np.all((max_per_band < umbral_max) & (max_per_band > umbral_min)):
            valid_idxs.append(i)
    # Si no hay shots válidos, devuelvo intensidades=None
    if not valid_idxs:
        print('Todos los espectros saturan')
        return ws, None, nombres
    
    # Extraigo los shots válidos 
    valid_shots = shots[valid_idxs, :, :]      # (K,4,N)

    # 4) Resto drk de cada shot
    valid_shots_corr = valid_shots - drk_arr[None, :, :]  # (k,4,N)
    
    # 8) Extraigo los shots válidos y promedio por banda
    avg_per_band = valid_shots_corr.mean(axis=0)         # (4,N)
    
    # 9) Descompongo en lista [UV1, UV2, VIS, NIR]
    intensidades = [avg_per_band[j] for j in range(avg_per_band.shape[0])]
    return ws, intensidades, nombres    


