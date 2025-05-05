import os
import sys
sys.path.append('C:/Users/elsam/Documents/GitHub/LIBS_QUANTIFICATION_INTA')
from LIBS_quantification_toolbox import * 
import numpy as np

# Directorio base donde se encuentran los datos
espectra = "Spectra"
base_dir = "FinalSamplesTrial/Level0"
nombre_base = "LV0"  # Ajusta si tus archivos tienen un patrón diferente

# Iterar sobre M1 a M28 y P1 a P3
for i in range(1, 29):
    carpeta_m = f"M{i}"
    for j in range(1, 4):
        carpeta_p = f"P{j}"
        ruta_relativa = os.path.join(espectra, base_dir, carpeta_m, carpeta_p)
        
        if not os.path.exists(ruta_relativa):
            print(f"Saltando {ruta_relativa}, no existe.")
            continue
        
        try:
            ruta_relativa2 = os.path.join(base_dir, carpeta_m, carpeta_p)
            ws, intensidades, nombres = cargar_espectros_5shotspromV2_0(ruta_relativa2, nombre_base = None)

            if intensidades is None:
                print(f"Saltando {ruta_relativa}, sin espectros válidos.")
                continue

            # Guardado tras preprocesado
            archivo_salida_preproc = ruta_relativa.replace("Level0", "Level1").replace("P", "PP") + "_preproc.txt"
            os.makedirs(os.path.dirname(archivo_salida_preproc), exist_ok=True)

            for i_band, (w, s) in enumerate(zip(ws, intensidades)):
                apply_preprocessing_and_save(s, w, archivo_salida_preproc.replace(".txt", f"_band{i_band}.txt"))

            # Guardar gráfico
            nombre_figura = archivo_salida_preproc.replace(".txt", ".png")
            plot_and_save_spectra(ws, intensidades, f"Espectros {carpeta_m}-{carpeta_p}", nombre_figura, nombres)

        except Exception as e:
            print(f"Error en {ruta_relativa}: {e}")
