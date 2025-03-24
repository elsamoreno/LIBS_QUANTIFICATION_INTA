#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Open spectrometer files 
def leer_archivo_txt(nombre_archivo, saltar_lineas=5, delimitador=';'):
    try:
        df = pd.read_csv(nombre_archivo, delimiter=delimitador, skiprows=saltar_lineas)
        df.columns = df.columns.str.strip()
        df['Wave'] = pd.to_numeric(df['Wave'], errors='coerce')
        df['Scope Corrected for Dark'] = pd.to_numeric(df['Scope Corrected for Dark'], errors='coerce')
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
def graficar_datos(df, columna_x, columna_y):
    
    plt.figure(figsize=(8, 5))
    plt.plot(df[columna_x], df[columna_y], marker='.', linestyle='-')
    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.title(f"Gráfica de {columna_y} vs {columna_x}")
    plt.grid()
    plt.show()


def graficar_multiples_dfs(lista_dfs, nombres, columna_x, columna_y):
    
    plt.figure(figsize=(8, 5))
    for df, nombre in zip(lista_dfs, nombres):
        if df is not None and columna_x in df.columns and columna_y in df.columns:
            plt.plot(df[columna_x], df[columna_y], marker='.', linestyle='-', markersize=3, linewidth=0.8, label=nombre)
        else:
            print(f"Error: No se pudo graficar {nombre}, columnas no encontradas")
    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.title(f"Gráfica de {columna_y} vs {columna_x} de los 4 espectrómetros")
    plt.legend()
    plt.minorticks_on()  # Habilitar las marcas menores
    plt.grid(which='both', linestyle='-', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    # Ajustar los márgenes de manera manual
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    plt.show()



UV1 = "2.E2E_olivine/Olivine_LIBS_shot01_7324767SP.txt" 
UV2 = "2.E2E_olivine/Olivine_LIBS_shot01_7324768SP.txt" 
VIS = "2.E2E_olivine/Olivine_LIBS_shot01_7324769SP.txt" 
NIR = "2.E2E_olivine/Olivine_LIBS_shot01_7324770SP.txt" 

datos_UV1 = leer_archivo_txt(UV1)
datos_UV2 = leer_archivo_txt(UV2)
datos_VIS = leer_archivo_txt(VIS)
datos_NIR = leer_archivo_txt(NIR)

if datos_UV1 is not None and datos_UV2 is not None and datos_VIS is not None and datos_NIR is not None:
    #print(datos_UV1.head())
    #archivos = [datos_UV1]
    # Lista de DataFrames y nombres
    dfs = [datos_UV1, datos_UV2, datos_VIS, datos_NIR]
    nombres = ["UV1", "UV2", "VIS", "NIR"]
    # Llamar a la función de graficado
    graficar_multiples_dfs(dfs, nombres, 'Wave', 'Scope Corrected for Dark')
else:
    print("Error")

# Definir los intervalos y los archivos asociados a cada uno
intervalos = {
    "Intervalo 1 (353.53-363.79 nm)": [datos_UV1, datos_UV2],   # Solo afecta UV1 y UV2
    "Intervalo 2 (450.96-463.86 nm)": [datos_UV2, datos_VIS],   # Solo afecta UV2 y VIS
    "Intervalo 3 (691.50-705.11 nm)": [datos_VIS, datos_NIR]    # Solo afecta VIS y NIR
}

# Calcular las medianas por intervalo y por archivo
medianas = {}

for intervalo, archivos in intervalos.items():
    medianas[intervalo] = {}  # Crear diccionario para cada intervalo
    
    for i, df in enumerate(archivos):
        if df is not None:
            min_wave, max_wave = map(float, intervalo.split("(")[1].split("nm")[0].split("-"))
            df_filtrado = df[(df['Wave'] >= min_wave) & (df['Wave'] <= max_wave)]
            
            if not df_filtrado.empty:
                mediana_y = df_filtrado['Scope Corrected for Dark'].median()
            else:
                mediana_y = None
            
            # Guardar la mediana asociada al archivo
            medianas[intervalo][f"Archivo {i+1}"] = mediana_y

# Imprimir los resultados
print("\nMedianas de 'Scope Corrected for Dark' en los intervalos de Wave:")
for intervalo, resultados in medianas.items():
    print(f"\n{intervalo}:")
    for archivo, mediana in resultados.items():
        print(f"  {archivo}: {mediana}")

# Calcular los coeficientes basados en las medianas
coeficientes = {}

for intervalo, resultados in medianas.items():
    # Verificamos que tengamos al menos dos archivos para calcular el coeficiente
    if len(resultados) >= 2:
        archivo_1, archivo_2 = list(resultados.values())[:2]  # Tomamos las medianas de los dos primeros archivos
        if archivo_1 is not None and archivo_2 is not None:
            # Calculamos el coeficiente
            coeficiente = archivo_1 / archivo_2  # Aquí puedes poner cualquier operación que desees
            coeficientes[intervalo] = coeficiente

# Imprimir los coeficientes calculados
print("\nCoeficientes calculados por intervalo:")
for intervalo, coeficiente in coeficientes.items():
    print(f"{intervalo}: {coeficiente}")