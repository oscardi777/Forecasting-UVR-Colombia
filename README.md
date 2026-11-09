# Forecasting-UVR-Colombia

Trabajo final de **Matemáticas Financieras**. Este repositorio contiene la solución
completa de los ejercicios del enunciado (`enunciado.pdf`): diseño de una estrategia de
inversión para cubrir un crédito en UVR (ejercicio 1) y dos ejercicios de moneda
extranjera (ejercicios 5 y 6).

La idea central del ejercicio 1 es: se tiene un capital inicial de **760.000.000 COP** y
un crédito en UVR a 10 años (cuotas mensuales + abonos extraordinarios). Como la UVR está
indexada a la inflación, primero se **pronostica la UVR** con tres modelos distintos, con
eso se construye el **flujo del pasivo en pesos** (`Lt`), y finalmente se arma un
**portafolio de inversión (ALM)** con tres activos (Bono, Fondo, ETF) que se optimiza con
Markowitz multiperiodo y se somete a un análisis de riesgo (shortfall) por Monte Carlo.

## Integrantes

- Oscar Andrés Díaz González
- Jerónimo Gil Giraldo
- Isaac Uribe

---

## ¿Dónde está la solución de cada ejercicio?

| Ejercicio | Archivo | Qué resuelve |
|-----------|---------|--------------|
| **1** (crédito UVR + portafolio) | [`modelos_python/main.ipynb`](modelos_python/main.ipynb) | Genera los activos, optimiza el portafolio ALM y hace el análisis de shortfall. Se apoya en los pronósticos de la UVR producidos por los demás notebooks. |
| **5** (inversión en CHF/BRL) | [`ejerciciosAdicionales.ipynb`](ejerciciosAdicionales.ipynb) | Rentabilidad efectiva en francos suizos y capital final. |
| **6** (financiación en MXN/PEN/USD) | [`ejerciciosAdicionales.ipynb`](ejerciciosAdicionales.ipynb) | Alternativa de crédito más barata en la moneda de la empresa (MXN). |

> **Notebook principal:** [`modelos_python/main.ipynb`](modelos_python/main.ipynb). Reúne en un
> solo lugar todo el flujo del ejercicio 1 (genera activos en memoria, optimiza el portafolio
> y analiza el riesgo) sin necesidad de archivos intermedios.

---

## Cómo se conecta todo (flujo de datos del ejercicio 1)

```
datos crudos (data/)
        │
        ▼
 Notebooks de pronóstico de la UVR          ──►  pronosticos_uvr/*.xlsx
  (ARIMA, SARIMAX, MBG)                           (UVR proyectada a 120 meses)
        │
        ▼
 cuotasUVR/cuotasUVR.csv  +  pronostico UVR
        │
        ▼
 cleaning/extraccion.py  (Lt = cuotaUVR * UVR_proyectada)
        │
        ▼
 flujosPronosticados/flujo_pronostico_uvr_*.csv   (pasivo Lt en COP)
        │
        ▼
 modelos_python/main.ipynb   (portafolio ALM + optimización + shortfall)
        │
        ▼
 plots/   (gráficas de resultados)
```

---

## Estructura del repositorio

### Notebooks (código)

- **`modelos_python/`** — Todos los modelos en Python.
  - [`main.ipynb`](modelos_python/main.ipynb) — **Solución del ejercicio 1.** Genera las
    trayectorias de los activos, estima `mu`/`Sigma`, optimiza el portafolio Markowitz
    multiperiodo (restricciones de riesgo y liquidez), proyecta el capital contra el pasivo
    y mide el riesgo de *shortfall* por Monte Carlo.
  - [`SimulacionArimaProyecto.ipynb`](modelos_python/SimulacionArimaProyecto.ipynb) —
    Pronóstico de la UVR con un modelo **ARIMA**.
  - [`SimulacionSarimaxProyecto.ipynb`](modelos_python/SimulacionSarimaxProyecto.ipynb) —
    Pronóstico de la UVR con un modelo **SARIMAX** (usa IPC y TRM como variables exógenas).
  - [`IEPMBGPEII20262.ipynb`](modelos_python/IEPMBGPEII20262.ipynb) — Pronóstico de la UVR
    con un **Movimiento Browniano Geométrico (MBG)**, con identificación, estimación,
    simulación y pruebas estadísticas.
  - [`activos_modelados.ipynb`](modelos_python/activos_modelados.ipynb) — Versión separada de
    la generación de trayectorias de los activos (Bono, Fondo, ETF). `main.ipynb` ya integra
    esta lógica, se conserva como referencia.
  - [`optimizacion_portafolio_ALM.ipynb`](modelos_python/optimizacion_portafolio_ALM.ipynb) —
    Versión separada de la optimización del portafolio ALM. También está integrada en
    `main.ipynb`.
- [`ejerciciosAdicionales.ipynb`](ejerciciosAdicionales.ipynb) — **Solución de los ejercicios
  5 y 6** (moneda extranjera).

### Datos de entrada

- **`data/`** — Series históricas crudas.
  - `datosUVR.xlsx`, `datosUVR_IPC_TRM.xlsx` — UVR histórica (y IPC/TRM para SARIMAX).
  - `UVR_daily.csv`, `UVR_mensual.csv` — UVR diaria y mensual ya procesadas.
- **`cuotasUVR/cuotasUVR.csv`** — Cuota del crédito expresada en UVR por periodo (base para
  construir el pasivo). Las primeras cuotas son `0` por el periodo de gracia de 3 años.
- **`ejercicioAmortizacion.xlsx`** — Tabla de amortización del crédito.

### Scripts de preparación

- **`cleaning/extraccion.py`** — Combina la cuota en UVR con la UVR proyectada de uno de los
  Excel de `pronosticos_uvr/` y genera el flujo del pasivo `Lt = cuotaUVR * UVR_proyectada`
  en `flujosPronosticados/`. Para cambiar el pronóstico base se edita la constante
  `ARCHIVO_EXCEL` dentro del script.

### Resultados generados

- **`pronosticos_uvr/`** — UVR proyectada a 120 meses por cada modelo:
  `pronostico_uvr_arima.xlsx`, `pronostico_uvr_mbg.xlsx`, `pronostico_uvr_Sarimax.xlsx`.
- **`flujosPronosticados/`** — Flujo del pasivo en COP (`periodo`, `Lt`) por cada pronóstico:
  `flujo_pronostico_uvr_arima.csv`, `flujo_pronostico_uvr_mbg.csv`,
  `flujo_pronostico_uvr_Sarimax.csv`. Son la entrada directa del portafolio en `main.ipynb`.
- **`pronosticosActivos/`** — Salidas opcionales de la generación de activos: `mu_activos.csv`,
  `Sigma_mensual.csv`, `Sigma_anual.csv`, trayectorias mensuales y resumen. Los archivos de
  trayectorias pesados (`.npz` y `trayectorias_mensuales_*.csv`) están en `.gitignore` porque
  superan el límite de GitHub; se regeneran ejecutando los notebooks.
- **`plots/`** — Gráficas producidas por los notebooks (evolución del portafolio, histogramas
  de residual, percentiles, tasas de cambio, etc.).

### Otros archivos

- **`enunciado.pdf`** — Enunciado del trabajo.
- **`main.tex`** — Documento LaTeX del informe.
- **`presentacion_notebookEdit.pptx`** — Diapositivas de la presentación.
- **`requirements.txt`** — Dependencias de Python.

---

## Instalación

Requiere **Python 3.11+** (el proyecto se desarrolló con 3.14).

1. Clonar el repositorio y entrar a la carpeta:

   ```powershell
   git clone <url-del-repositorio>
   cd Forecasting-UVR-Colombia
   ```

2. Crear y activar un entorno virtual:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

---

## Cómo reproducir los resultados

### Opción rápida: ejecutar solo lo necesario

Los pronósticos de la UVR y los flujos del pasivo ya están versionados en
`pronosticos_uvr/` y `flujosPronosticados/`. Para reproducir el ejercicio 1 basta con abrir
y ejecutar de arriba a abajo:

```powershell
jupyter lab
```

y correr [`modelos_python/main.ipynb`](modelos_python/main.ipynb). Allí puedes cambiar en la
sección de parámetros el capital inicial, el número de trayectorias `K`, las rentabilidades
de los activos y el flujo del pasivo (`ARCHIVO_FLUJO`: mbg / arima / sarimax).

Para los ejercicios 5 y 6, ejecuta
[`ejerciciosAdicionales.ipynb`](ejerciciosAdicionales.ipynb) de arriba a abajo.

### Opción completa: regenerar todo desde los datos crudos

1. **Pronosticar la UVR.** Ejecuta los tres notebooks de pronóstico. Cada uno escribe su
   Excel en `pronosticos_uvr/`:
   - `modelos_python/SimulacionArimaProyecto.ipynb`
   - `modelos_python/SimulacionSarimaxProyecto.ipynb`
   - `modelos_python/IEPMBGPEII20262.ipynb`

2. **Construir el flujo del pasivo.** Para cada pronóstico, edita la constante
   `ARCHIVO_EXCEL` en `cleaning/extraccion.py` y ejecútalo:

   ```powershell
   python cleaning/extraccion.py
   ```

   Esto genera el `flujo_pronostico_uvr_*.csv` correspondiente en `flujosPronosticados/`.

3. **Portafolio y análisis de riesgo.** Ejecuta `modelos_python/main.ipynb` de arriba a
   abajo. Produce la tabla de pesos óptimos por periodo, la evolución del portafolio frente
   al pasivo, el análisis de shortfall y las gráficas en `plots/`.

> **Nota sobre los notebooks de pronóstico:** algunos leen las rutas de los datos de forma
> relativa a su propia ubicación (p. ej. `../data/UVR_mensual.csv`). Ejecútalos desde
> `modelos_python/` o con Jupyter abierto en la raíz del proyecto para que las rutas
> resuelvan correctamente.

---

## Notas

- El optimizador del portafolio usa `cvxpy` si está instalado y, si no, cae automáticamente
  a `scipy.optimize` (SLSQP). `requirements.txt` incluye `scipy`, así que funciona sin
  `cvxpy`.
- Los resultados de las simulaciones Monte Carlo son reproducibles gracias a las semillas
  fijadas en cada notebook.
