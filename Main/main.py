import sys
sys.path.append('C:/Users/elsam/Documents/GitHub/LIBS_QUANTIFICATION_INTA')
from LIBS_quantification_toolbox import * 
import numpy as np

#espectro, longitud_de_onda, nombres = cargar_espectros("20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position1", "Pellet-T1_position1_Burst5-n1" ) 

#nombres, lambdas, n1, n2, n3, n4, n5 = cargar_espectros_5shots("../Spectra/20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position2", "Pellet-T1_position2_Burst5")

#Lectura datos T1
nombres, lambdas1, UV1_T1_P1, UV2_T1_P1, VIS_T1_P1, NIR_T1_P1 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P1", "Pellet-T1_position1_Burst5")
nombres, lambdas2, UV1_T1_P2, UV2_T1_P2, VIS_T1_P2, NIR_T1_P2 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P2", "Pellet-T1_position2_Burst5")
nombres, lambdas3, UV1_T1_P3, UV2_T1_P3, VIS_T1_P3, NIR_T1_P3 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M1/P3", "Pellet-T1_position3_Burst5")
#Lectura datos T2
nombres, lambdas4, UV1_T2_P1, UV2_T2_P1, VIS_T2_P1, NIR_T2_P1 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P1", "Pellet_position1_Burst5")
nombres, lambdas5, UV1_T2_P2, UV2_T2_P2, VIS_T2_P2, NIR_T2_P2 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P2", "Pellet_position2_Burst5")
nombres, lambdas6, UV1_T2_P3, UV2_T2_P3, VIS_T2_P3, NIR_T2_P3 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M2/P3", "Pellet_position3_Burst5")
#Lectura datos T3
nombres, lambdas7, UV1_T3_P1, UV2_T3_P1, VIS_T3_P1, NIR_T3_P1 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P1", "Pellet-T3_position1_Burst5")
nombres, lambdas8, UV1_T3_P2, UV2_T3_P2, VIS_T3_P2, NIR_T3_P2 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P2", "Pellet-T3_position2_Burst5")
nombres, lambdas9, UV1_T3_P3, UV2_T3_P3, VIS_T3_P3, NIR_T3_P3 = cargar_espectros_5shotsprom("../Spectra/FinalSamplesTrial/Level0/M3/P3", "Pellet-T3_position3_Burst5")

#processed_spectra_T1_P1, ws1 = apply_preprocessing([UV1_T1_P1, UV2_T1_P1, VIS_T1_P1, NIR_T1_P1], lambdas)
#processed_spectra_T1_P2, ws2 = apply_preprocessing([UV1_T1_P2, UV2_T1_P2, VIS_T1_P2, NIR_T1_P2], lambdas)
#processed_spectra_T1_P3, ws3 = apply_preprocessing([UV1_T1_P3, UV2_T1_P3, VIS_T1_P3, NIR_T1_P3], lambdas)
#processed_spectra_T2_P1, ws4 = apply_preprocessing([UV1_T2_P1, UV2_T2_P1, VIS_T2_P1, NIR_T2_P1], lambdas)
#processed_spectra_T2_P3, ws5 = apply_preprocessing([UV1_T2_P3, UV2_T2_P3, VIS_T2_P3, NIR_T2_P3], lambdas)
#processed_spectra_T3_P1, ws6 = apply_preprocessing([UV1_T3_P1, UV2_T3_P1, VIS_T3_P1, NIR_T3_P1], lambdas)
#processed_spectra_T3_P2, ws7 = apply_preprocessing([UV1_T3_P2, UV2_T3_P1, VIS_T3_P2, NIR_T3_P2], lambdas)



#plot_multiple_spectra_vertical([ws1, ws2, ws3], 
#                      [processed_spectra_T1_P1, processed_spectra_T1_P2, processed_spectra_T1_P3], 
#                      "Espectros de LIBS", 
#                      nombres=["T1 P1", "T1 P2", "T1 P3"])
