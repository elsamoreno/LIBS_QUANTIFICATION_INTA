import sys
sys.path.append('C:/Users/elsam/Documents/GitHub/LIBS_QUANTIFICATION_INTA')
from LIBS_quantification_toolbox import * 
import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Lectura datos T1 y guardar
lambdas_T1_P1, espectros_T1_P1, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M1", "P1"), "Pellet-T1_position1_Burst5")
lambdas_T1_P2, espectros_T1_P2, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M1", "P2"), "Pellet-T1_position2_Burst5")
lambdas_T1_P3, espectros_T1_P3, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M1", "P3"), "Pellet-T1_position3_Burst5")
#Lectura datos T2
lambdas_T2_P1, espectros_T2_P1, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M2", "P1"), "Pellet_position1_Burst5")
lambdas_T2_P2, espectros_T2_P2, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M2", "P2"), "Pellet_position2_Burst5")
lambdas_T2_P3, espectros_T2_P3, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M2", "P3"), "Pellet_position3_Burst5")
#Lectura datos T3
lambdas_T3_P1, espectros_T3_P1, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M3", "P1"), "Pellet-T3_position1_Burst5")
lambdas_T3_P2, espectros_T3_P2, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M3", "P2"), "Pellet-T3_position2_Burst5")
lambdas_T3_P3, espectros_T3_P3, nombres = cargar_espectros_5shotsprom(os.path.join(BASE_DIR, "..", "Spectra", "FinalSamplesTrial", "Level0", "M3", "P3"), "Pellet-T3_position3_Burst5")

ws1, processed_spectra_T1_P1 = apply_preprocessing_and_save(espectros_T1_P1, lambdas_T1_P1, "../Spectra/FinalSamplesTrial/Level2/LV2_M1_P1.txt")
ws2, processed_spectra_T1_P2 = apply_preprocessing_and_save(espectros_T1_P2, lambdas_T1_P2, "../Spectra/FinalSamplesTrial/Level2/LV2_M1_P2.txt")
ws3, processed_spectra_T1_P3 = apply_preprocessing_and_save(espectros_T1_P3, lambdas_T1_P3, "../Spectra/FinalSamplesTrial/Level2/LV2_M1_P3.txt")
ws4, processed_spectra_T2_P1 = apply_preprocessing_and_save(espectros_T2_P1, lambdas_T2_P1, "../Spectra/FinalSamplesTrial/Level2/LV2_M2_P1.txt")
ws5, processed_spectra_T2_P2 = apply_preprocessing_and_save(espectros_T2_P2, lambdas_T2_P2, "../Spectra/FinalSamplesTrial/Level2/LV2_M2_P2.txt")
ws6, processed_spectra_T2_P3 = apply_preprocessing_and_save(espectros_T2_P3, lambdas_T2_P3, "../Spectra/FinalSamplesTrial/Level2/LV2_M2_P3.txt")
ws7, processed_spectra_T3_P1 = apply_preprocessing_and_save(espectros_T3_P1, lambdas_T3_P1, "../Spectra/FinalSamplesTrial/Level2/LV2_M3_P1.txt")
ws8, processed_spectra_T3_P2 = apply_preprocessing_and_save(espectros_T3_P2, lambdas_T3_P2, "../Spectra/FinalSamplesTrial/Level2/LV2_M3_P2.txt")
#ws9, processed_spectra_T3_P3 = apply_preprocessing(espectros_T3_P3, lambdas_T3_P3)
print(espectros_T3_P3)


#Guardar imágemes NIVEL-1
plot_and_save_spectra(lambdas_T1_P1, espectros_T1_P1, "T1-P1", "Spectra/FinalSamplesTrial/Level1/LV1_T1_P1.png", nombres)
plot_and_save_spectra(lambdas_T1_P2, espectros_T1_P2, "T1-P2", "Spectra/FinalSamplesTrial/Level1/LV1_T1_P2.png", nombres)
plot_and_save_spectra(lambdas_T1_P3, espectros_T1_P3, "T1-P3", "Spectra/FinalSamplesTrial/Level1/LV1_T1_P3.png", nombres)
plot_and_save_spectra(lambdas_T2_P1, espectros_T2_P1, "T2-P1", "Spectra/FinalSamplesTrial/Level1/LV1_T2_P1.png", nombres)
plot_and_save_spectra(lambdas_T2_P2, espectros_T2_P2, "T2-P2", "Spectra/FinalSamplesTrial/Level1/LV1_T2_P2.png", nombres)
plot_and_save_spectra(lambdas_T2_P3, espectros_T2_P3, "T2-P3", "Spectra/FinalSamplesTrial/Level1/LV1_T2_P3.png", nombres)
plot_and_save_spectra(lambdas_T3_P1, espectros_T3_P1, "T3-P1", "Spectra/FinalSamplesTrial/Level1/LV1_T3_P1.png", nombres)
plot_and_save_spectra(lambdas_T3_P2, espectros_T3_P2, "T3-P2", "Spectra/FinalSamplesTrial/Level1/LV1_T3_P2.png", nombres)
#plot_and_save_spectra(lambdas_T3_P3, espectros_T3_P3, "T3-P3", "../Spectra/FinalSamplesTrial/Level1/LV1_T3_P3.png", nombres)
#Guardar imágenes NIVEL-1 superpuestas
plot_and_save_spectra([lambdas_T1_P1, lambdas_T1_P2, lambdas_T1_P3], [espectros_T1_P1, espectros_T1_P2, espectros_T1_P3], "T1 - Comparación de los 3 spots", "Spectra/FinalSamplesTrial/Level1/LV1_T1_P1-2-3.png", ["P1","P2","P3"])
plot_and_save_spectra([lambdas_T2_P1, lambdas_T2_P2, lambdas_T2_P3], [espectros_T2_P1, espectros_T2_P2, espectros_T2_P3], "T2 - Comparación de los 3 spots", "Spectra/FinalSamplesTrial/Level1/LV1_T2_P1-2-3.png", ["P1","P2","P3"])
plot_and_save_spectra([lambdas_T3_P1, lambdas_T3_P2], [espectros_T3_P1, espectros_T3_P2], "T3 - Comparación de los 2 spots", "Spectra/FinalSamplesTrial/Level1/LV1_T3_P1-2-3.png", ["P1","P2"])

#Guardar imágenes NIVEL-2
plot_and_save_spectra(ws1, processed_spectra_T1_P1, "T1-P1-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T1_P1.png")
plot_and_save_spectra(ws2, processed_spectra_T1_P2, "T1-P2-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T1_P2.png")
plot_and_save_spectra(ws3, processed_spectra_T1_P3, "T1-P3-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T1_P3.png")
plot_and_save_spectra(ws4, processed_spectra_T2_P1, "T2-P1-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T2_P1.png")
plot_and_save_spectra(ws5, processed_spectra_T2_P2, "T2-P2-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T2_P2.png")
plot_and_save_spectra(ws6, processed_spectra_T2_P3, "T2-P3-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T2_P3.png")
plot_and_save_spectra(ws7, processed_spectra_T3_P1, "T3-P1-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T3_P1.png")
plot_and_save_spectra(ws8, processed_spectra_T3_P2, "T3-P2-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T3_P2.png")
#Guardar imágenes NIVEL-2 superpuestas
plot_and_save_spectra([ws1,ws2,ws3], [processed_spectra_T1_P1,processed_spectra_T1_P2,processed_spectra_T1_P3], "T1-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T1_P1-2-3.png", ["P1", "P2", "P3"])
plot_and_save_spectra([ws4,ws5,ws6], [processed_spectra_T2_P1,processed_spectra_T2_P2,processed_spectra_T2_P3], "T2-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T2_P1-2-3.png", ["P1", "P2", "P3"])
plot_and_save_spectra([ws7,ws8], [processed_spectra_T3_P1,processed_spectra_T3_P2], "T3-Preprocessed", "Spectra/FinalSamplesTrial/Level2/LV2_T3_P1-2-3.png", ["P1", "P2"])


