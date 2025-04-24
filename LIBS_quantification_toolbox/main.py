from lectura import cargar_espectros
from lectura import cargar_espectros_5shots
from lectura import cargar_espectros_5shotsprom

espectro, longitud_de_onda, nombres = cargar_espectros("../Spectra/20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position1", "Pellet-T1_position1_Burst5-n1" ) 

nombres, lambdas, n1, n2, n3, n4, n5 = cargar_espectros_5shots("../Spectra/20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position1", "Pellet-T1_position1_Burst5")

nombres, lambdas, UV1_prom, UV2_prom, VIS_prom, NIR_prom = cargar_espectros_5shotsprom("../Spectra/20250328_OHO-SN3_LIBS-Quantif_samples/2.Pellet_T1/Position1", "Pellet-T1_position1_Burst5")

