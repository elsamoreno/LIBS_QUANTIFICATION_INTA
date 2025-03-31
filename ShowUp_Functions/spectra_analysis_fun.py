import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from offset_fun import get_corrected_spectra
from tools_funs import graficar_multiples_dfs_32


### 5 shot representation

def five_shot_representation(data_UV1_5shots, data_UV2_5shots, data_VIS_5shots, data_NIR_5shots):
    # 1: REPRESENTACIÓN AISLADA DE CADA SHOT
    data_UV1_n1 = data_UV1_5shots[0]
    data_UV2_n1 = data_UV2_5shots[0]
    data_VIS_n1 = data_VIS_5shots[0]
    data_NIR_n1 = data_NIR_5shots[0]
    data_UV1_n2 = data_UV1_5shots[1]
    data_UV2_n2 = data_UV2_5shots[1]
    data_VIS_n2 = data_VIS_5shots[1]
    data_NIR_n2 = data_NIR_5shots[1]
    data_UV1_n3 = data_UV1_5shots[2]
    data_UV2_n3 = data_UV2_5shots[2]
    data_VIS_n3 = data_VIS_5shots[2]
    data_NIR_n3 = data_NIR_5shots[2]
    data_UV1_n4 = data_UV1_5shots[3]
    data_UV2_n4 = data_UV2_5shots[3]
    data_VIS_n4 = data_VIS_5shots[3]
    data_NIR_n4 = data_NIR_5shots[3]
    data_UV1_n5 = data_UV1_5shots[4]
    data_UV2_n5 = data_UV2_5shots[4]
    data_VIS_n5 = data_VIS_5shots[4]
    data_NIR_n5 = data_NIR_5shots[4]
    data_UV1_n1_corr,data_UV2_n1_corr,data_VIS_n1_corr,data_NIR_n1_corr = get_corrected_spectra(data_UV1_n1, data_UV2_n1, data_VIS_n1, data_NIR_n1)
    data_UV1_n2_corr,data_UV2_n2_corr,data_VIS_n2_corr,data_NIR_n2_corr = get_corrected_spectra(data_UV1_n2, data_UV2_n2, data_VIS_n2, data_NIR_n2)
    data_UV1_n3_corr,data_UV2_n3_corr,data_VIS_n3_corr,data_NIR_n3_corr = get_corrected_spectra(data_UV1_n3, data_UV2_n3, data_VIS_n3, data_NIR_n3)
    data_UV1_n4_corr,data_UV2_n4_corr,data_VIS_n4_corr,data_NIR_n4_corr = get_corrected_spectra(data_UV1_n4, data_UV2_n4, data_VIS_n4, data_NIR_n4)
    data_UV1_n5_corr,data_UV2_n5_corr,data_VIS_n5_corr,data_NIR_n5_corr = get_corrected_spectra(data_UV1_n5, data_UV2_n5, data_VIS_n5, data_NIR_n5)
    dfs1 = [data_UV1_n1_corr, data_UV2_n1_corr, data_VIS_n1_corr, data_NIR_n1_corr]
    names1 = ["UV1", "UV2", "VIS", "NIR "]
    graficar_multiples_dfs_32(dfs1, names1, "Position X - n1", 'Wave', 'Sample')
    dfs2 = [data_UV1_n2_corr, data_UV2_n2_corr, data_VIS_n2_corr, data_NIR_n2_corr]
    names2 = ["UV1", "UV2", "VIS", "NIR "]
    graficar_multiples_dfs_32(dfs2, names2, "Position X - n2", 'Wave', 'Sample')
    dfs3 = [data_UV1_n3_corr, data_UV2_n3_corr, data_VIS_n3_corr, data_NIR_n3_corr]
    names3 = ["UV1", "UV2", "VIS", "NIR "]
    graficar_multiples_dfs_32(dfs3, names3, "Position X - n3", 'Wave', 'Sample')
    dfs4 = [data_UV1_n4_corr, data_UV2_n4_corr, data_VIS_n4_corr, data_NIR_n4_corr]
    names4 = ["UV1", "UV2", "VIS", "NIR "]
    graficar_multiples_dfs_32(dfs4, names4, "Position X - n4", 'Wave', 'Sample')
    dfs5 = [data_UV1_n5_corr, data_UV2_n5_corr, data_VIS_n5_corr, data_NIR_n5_corr]
    names5 = ["UV1", "UV2", "VIS", "NIR "]
    graficar_multiples_dfs_32(dfs5, names5, "Position X - n5", 'Wave', 'Sample')

    # REPRESENTACIÓN SUPERPUESTA DE LOS 5 SHOTS EN LONGITUD DE ONDA
    dfs_UV1 = [data_UV1_n1, data_UV1_n2, data_UV1_n3, data_UV1_n4, data_UV1_n5]
    names_UV1 = ["UV1-n1", "UV1-n2", "UV1-n3", "UV1-n4", "UV1-n5"]
    graficar_multiples_dfs_32(dfs_UV1, names_UV1, "Position X - UV1", 'Wave', 'Sample')

    dfs_UV2 = [data_UV2_n1, data_UV2_n2, data_UV2_n3, data_UV2_n4, data_UV2_n5]
    names_UV2 = ["UV2-n1", "UV2-n2", "UV2-n3", "UV2-n4", "UV2-n5"]
    graficar_multiples_dfs_32(dfs_UV2, names_UV2, "Position X - UV2", 'Wave', 'Sample')

    dfs_VIS = [data_VIS_n1, data_VIS_n2, data_VIS_n3, data_VIS_n4, data_VIS_n5]
    names_VIS = ["VIS-n1", "VIS-n2", "VIS-n3", "VIS-n4", "VIS-n5"]
    graficar_multiples_dfs_32(dfs_VIS, names_VIS, "Position X - VIS", 'Wave', 'Sample')

    dfs_NIR = [data_NIR_n1, data_NIR_n2, data_NIR_n3, data_NIR_n4, data_NIR_n5]
    names_NIR = ["NIR-n1", "NIR-n2", "NIR-n3", "NIR-n4", "NIR-n5"]
    graficar_multiples_dfs_32(dfs_NIR, names_NIR, "Position X - NIR", 'Wave', 'Sample')
    return