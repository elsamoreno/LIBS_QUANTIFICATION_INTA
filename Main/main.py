import sys
sys.path.append('C:/Users/elsam/Documents/GitHub/LIBS_QUANTIFICATION_INTA')
from LIBS_quantification_toolbox import * 
import numpy as np

#espectro, longitud_de_onda, nombres = cargar_espectros("20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position1", "Pellet-T1_position1_Burst5-n1" ) 

#nombres, lambdas, n1, n2, n3, n4, n5 = cargar_espectros_5shots("../Spectra/20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position2", "Pellet-T1_position2_Burst5")

#Lectura datos T1
lambdas_T1_P1, espectros_T1_P1, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P1", "Pellet-T1_position1_Burst5")
lambdas_T1_P2, espectros_T1_P2, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P2", "Pellet-T1_position2_Burst5")
lambdas_T1_P3, espectros_T1_P3, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P3", "Pellet-T1_position3_Burst5")
#Lectura datos T2
lambdas_T2_P1, espectros_T2_P1, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P1", "Pellet_position1_Burst5")
lambdas_T2_P2, espectros_T2_P2, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P2", "Pellet_position2_Burst5")
lambdas_T2_P3, espectros_T2_P3, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P3", "Pellet_position3_Burst5")
#Lectura datos T3
lambdas_T3_P1, espectros_T3_P1, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P1", "Pellet-T3_position1_Burst5")
lambdas_T3_P2, espectros_T3_P2, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P2", "Pellet-T3_position2_Burst5")
lambdas_T3_P3, espectros_T3_P3, nombres = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P3", "Pellet-T3_position3_Burst5")

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



plot_and_save_spectra(lambdas_T1_P1, espectros_T1_P1, "T1-P1", "../Spectra/FinalSamplesTrial/Level1/LV1_T1_P1.png", nombres)
plot_and_save_spectra(lambdas_T1_P1, espectros_T1_P1, "T1-P1", "../Spectra/FinalSamplesTrial/Level1/LV1_T1_P1.png", nombres)

