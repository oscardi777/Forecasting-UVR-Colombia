"""
Generacion de flujos pronosticados (Lt) en pesos.

Combina la cuota en UVR del archivo `cuotasUVR/cuotasUVR.csv` con la UVR
proyectada de uno de los archivos de pronostico en la carpeta
`pronosticos_uvr/` y produce un CSV con las columnas:
    - periodo  (1 a 120, se rellena automaticamente)
    - Lt       (cuotaUVR * UVR_Proyectada)

El resultado se guarda en la carpeta `flujosPronosticados/`.

Para ejecutarlo sobre otro archivo de pronostico basta con cambiar el nombre
en la constante ARCHIVO_EXCEL.
"""

from pathlib import Path

import pandas as pd

# --- Rutas ------------------------------------------------------------------
# El script vive en <proyecto>/cleaning/, por lo que la raiz es su carpeta padre.
BASE_DIR = Path(__file__).resolve().parent.parent

# Archivo de pronostico de UVR a usar. Cambiar este nombre para generar el
# flujo con cualquiera de los tres archivos disponibles:
#   - pronostico_uvr_arima.xlsx
#   - pronostico_uvr_mbg.xlsx
#   - pronostico_uvr_Sarimax.xlsx
ARCHIVO_EXCEL = BASE_DIR / "pronosticos_uvr" / "pronostico_uvr_Sarimax.xlsx"

# CSV con las cuotas en UVR (columna 'cuotaUVR').
ARCHIVO_CUOTAS = BASE_DIR / "cuotasUVR" / "cuotasUVR.csv"

# Salida: el CSV toma el nombre del archivo de pronostico de origen.
CARPETA_SALIDA = BASE_DIR / "flujosPronosticados"
ARCHIVO_SALIDA = CARPETA_SALIDA / f"flujo_{ARCHIVO_EXCEL.stem}.csv"

# --- Parametros de extraccion (numeracion de Excel) -------------------------
# La UVR proyectada esta en la columna B a partir de la fila 2 (la fila 1 es
# el encabezado). En indices 0-based de pandas: columna B = 1.
COL_UVR = 1        # columna B
FILA_INICIO = 2    # primera fila de datos (numeracion de Excel)


def extraer_uvr_proyectada() -> pd.Series:
    """Lee la columna B (UVR proyectada) del Excel desde la fila 2."""
    # header=None para trabajar con posiciones crudas; skiprows salta el
    # encabezado de la fila 1.
    df = pd.read_excel(
        ARCHIVO_EXCEL,
        header=None,
        usecols=[COL_UVR],
        skiprows=FILA_INICIO - 1,
        engine="openpyxl",
    )
    serie = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    return serie.reset_index(drop=True)


def extraer_cuotas_uvr() -> pd.Series:
    """Lee la columna 'cuotaUVR' del CSV de cuotas."""
    df = pd.read_csv(ARCHIVO_CUOTAS)
    return df["cuotaUVR"].reset_index(drop=True)


def calcular_flujos() -> pd.DataFrame:
    """Calcula Lt = cuotaUVR * UVR_Proyectada por periodo."""
    cuota_uvr = extraer_cuotas_uvr()
    uvr_proyectada = extraer_uvr_proyectada()

    n = min(len(cuota_uvr), len(uvr_proyectada))
    if len(cuota_uvr) != len(uvr_proyectada):
        print(
            "Advertencia: cuotaUVR tiene "
            f"{len(cuota_uvr)} filas y UVR proyectada {len(uvr_proyectada)}. "
            f"Se usaran las primeras {n}."
        )

    cuota_uvr = cuota_uvr.iloc[:n]
    uvr_proyectada = uvr_proyectada.iloc[:n]

    lt = cuota_uvr.values * uvr_proyectada.values

    df = pd.DataFrame({
        "periodo": range(1, n + 1),
        "Lt": lt,
    })
    return df


def main() -> None:
    df = calcular_flujos()

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8")

    print(f"Archivo de pronostico usado: {ARCHIVO_EXCEL.name}")
    print(f"Filas generadas: {len(df)}")
    print(f"Archivo guardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
