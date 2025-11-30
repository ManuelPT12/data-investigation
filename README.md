# Análisis Exploratorio de Datos (EDA) — Evolución de Mercados Financieros (2019–2025)

El objetivo del proyecto es realizar un **análisis exploratorio inicial (EDA)** sobre un dataset real, aplicando técnicas básicas de limpieza y visualización para comprender mejor su contenido.

---

## 1. Dataset utilizado

Para este ejercicio he trabajado con datos históricos descargados desde **Yahoo Finance** empleando la librería `yfinance`. El dataset recoge precios diarios de:

- Grandes empresas tecnológicas e IA (NVDA, MSFT, GOOG…)
- Empresas relacionadas con defensa, energía y chips
- Índices bursátiles globales (S&P500, Nikkei, EuroStoxx…)
- Materias primas como oro, petróleo o gas
- Criptomonedas (BTC, ETH, SOL)
- Activos relacionados con España (IBEX, EWP, bancos…)

 **Periodo analizado:** septiembre 2019 a noviembre 2025  
Este intervalo incluye eventos relevantes como COVID-19, inflación global, conflictos geopolíticos y el crecimiento del sector IA.

Los datos están en formato **largo**, donde cada fila representa un día y un ticker.

---

## 2. Pasos realizados en el análisis

Todo el desarrollo está en el notebook `notebooks/eda.ipynb`.

### Exploración inicial
- Inspección de filas, columnas y tipos de datos  
- Detección de valores faltantes  
- Búsqueda de duplicados  
- Revisión de rangos de precios y volúmenes  
- Identificación de incoherencias (volumen = 0, precios distorsionados…)

### Limpieza aplicada
El dataset estaba muy limpio originalmente, así que lo ensucié voluntariamente:
- Valores nulos aleatorios en columnas numéricas  
- Valores de volumen = 0  
- Outliers exagerados en la columna close

Esto me permitió trabajar todas las fases de limpieza:

- Imputación del volumen por ticker usando forward/backward fill  
- Eliminación de outliers muy extremos (por encima del cuantil 0.999)  
- Normalización de tipos de datos  
- Reordenación de columnas y estructura final del dataset

---

## 3. Visualizaciones incluidas

El notebook incluye las visualizaciones obligatorias:

### Histograma  
- Distribución del precio de cierre (antes de limpieza)

### Gráfica de barras  
- Comparación de rendimientos acumulados en activos españoles (IBEX, EWP, bancos…)

### Visualización adicional relevante  
- Evolución mensual normalizada por grupos:
  - sector IA / chips  
  - índices globales por región  
  - criptomonedas  
  - comparativa IBEX vs EWP  
  - Bitcoin vs Oro  

Estas gráficas permiten observar tendencias amplias del mercado y diferencias claras entre regiones y tipos de activos.

---

## 4. Estructura del repositorio

```bash

C:.
│   README.md
│   requirements.txt
│
├───data
│   ├───processed
│   │       prices_clean.csv
│   │
│   └───raw
│           prices_2019_2025.csv
│           prices_dirty_2019_2025.csv
│
├───notebooks
│       eda_prices.ipynb
│
└───src
        build_prices_dataset.py

```

---

## 5. Fuente de los datos

- Yahoo Finance — mediante la librería `yfinance`

---

## 6. Conclusiones exploratorias

- El dataset contiene un gran número de activos de distintos sectores, lo que permite comparar regiones, industrias y clases de activos.  
- La exploración inicial mostró valores faltantes, volumen cero y algunos precios distorsionados (outliers).  
- Tras limpiar los datos, se obtuvo una estructura coherente y lista para análisis temporal.  
- Las visualizaciones muestran que:
  - El sector IA y chips (especialmente NVIDIA) ha tenido un crecimiento excepcional (riesgo de burbuja, ya que no es normal que una empresa del mercado tenga el mismo valor que las 10 siguientes a ella JUNTAS).
  - Los índices globales se comportan de forma distinta por región: EEUU lidera, Europa es más estable, Asia más volátil.
  - Las criptomonedas presentan movimientos mucho más volátiles que los mercados tradicionales.
  - EWP ha rendido mejor que el IBEX, en parte por su composición y por el efecto de cotizar en dólares.
  - La Comparación del oro vs dólar. Podemos ver un síntoma de la inflación, el dólar cada día esta menos respaldado por el oro. Debido al miedo a una crisis global el precio del oro no para de subir.
  - Oro y Bitcoin se comportan de forma muy diferente: Bitcoin es especulativo y el oro actúa como refugio.

En conjunto, el EDA permite tener una visión clara de la estructura, problemas y tendencias del dataset, cumpliendo todos los requisitos del ejercicio.

---

**Fin del README**
