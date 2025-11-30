from pathlib import Path
import pandas as pd
import numpy as np
import yfinance as yf

DATA_DIR = Path("data")

TICKERS = [
    # Empresas de IA / Musk / geopolítica / energía / chips
    "NVDA", "MSFT", "GOOG", "META", "AMD",      # IA
    "PLTR",                                     # IA defensa / datos
    "TSLA",                                     # Muy importante, aunque no la use en el proyecto por falta de tiempo :(
    "LMT", "RTX",                               # defensa
    "XOM", "CVX",                               # energía (XOM petroleo, CVX gas)
    "ASML", "TSM",                              # chips

    # Índices y riesgo global / dólar / oro
    "^GSPC", "^NDX", "^VIX",                    # SP500, Nasdaq100, volatilidad del mercado
    "DX-Y.NYB",                                 # índice dólar (DXY)
    "GC=F",                                     # oro (futuros)

    # Más importantes USA
    "AAPL", "AMZN", "JPM", "UNH", "JNJ",
    "AVGO", "BAC", "WMT", "PEP", "KO",

    # Mercados de Salud / medicina / biofarma
    "MRNA", "PFE", "BNTX", "ABBV",
    "LLY", "GILD", "TMO", "REGN",

    #Industriales / infra / transporte
    "CAT", "DE", "HON", "GE", "MMM",
    "UPS", "FDX", "BA", "NEE", "DUK",

    #Materias primas
    "CL=F",    # petróleo crudo
    "NG=F",    # gas natural
    "SI=F",    # plata
    "HG=F",    # cobre
    "ZW=F",    # trigo

    #Índices globales
    "^FTSE",       # UK
    "^N225",       # Nikkei Japón
    "^HSI",        # Hong Kong
    "^STOXX50E",   # EuroStoxx 50

    # Cripto
    "BTC-USD", "ETH-USD", "SOL-USD",

    #España
    "^IBEX",       # IBEX 35
    "EWP",         # ETF España (MSCI Spain)
    "SAN",         # Banco Santander (ADR)
    "BBVA",        # BBVA (ADR)
    "TEF",         # Telefónica (ADR)
]

#Escojo estas fechas ya que creo que se han vivido situaciones críticas en el mundo, pudiendo ver así como ha reaccionado el mercado
START = "2019-09-01"
END = "2025-11-25"


def ensuciar_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    El dataset que cargo esta muy limpio, lo ensucio a propósito para poder cumplir con el ejercicioç
    ya que me apasiona el mercado y me entusiasmaba hacer el ejercicio sobre estos datos
      - meto NaN aleatorios en columnas numéricas
      - añado algunos outliers en 'close'
      - pongo volumen = 0 en parte de las filas
    """
    np.random.seed(42)
    df_dirty = df.copy()

    num_cols = ["open", "high", "low", "close", "adj_close", "volume"]

    # NaN aleatorios, aprox. 2% de las filas en cada columna
    for col in num_cols:
        mask = np.random.rand(len(df_dirty)) < 0.02
        df_dirty.loc[mask, col] = pd.NA

    # Outliers en 'close' multiplicamos algunas filas por 6
    n_outliers = 50
    idx_out = df_dirty.sample(n_outliers, random_state=42).index
    df_dirty.loc[idx_out, "close"] = df_dirty.loc[idx_out, "close"] * 6

    # Volumen = 0 en aprox. el 3% de las filas
    mask_zero = np.random.rand(len(df_dirty)) < 0.03
    df_dirty.loc[mask_zero, "volume"] = 0

    return df_dirty


def build_prices_dataset() -> None:
    """
    Descargo precios desde Yahoo Finance (muy fiable), deja el dataset en formato largo para
    poder meter ticker y guarda dos versiones:
      - prices_2019_2025.csv  -> datos tal cual, no lo uso pero no esta mal tener un resguardo
      - prices_dirty_2019_2025.csv -> le añadimos el ruido, este es el que usaré
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw_dir = DATA_DIR / "raw"
    raw_dir.mkdir(exist_ok=True)

    print(f"Descargando datos desde Yahoo Finance ({START} -> {END})...")
    data = yf.download(TICKERS, start=START, end=END)

    # De formato ancho (MultiIndex) a formato largo: una fila por fecha/ticker
    df = data.stack(level=1).reset_index()

    # Normalizar nombres de columnas
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    # Renombrar columnas clave
    df = df.rename(columns={"date": "date", "level_1": "ticker"})

    # Asegurar columna adj_close
    if "adj_close" not in df.columns:
        df["adj_close"] = df["close"]

    # Columnas que queremos sí o sí
    expected_cols = [
        "date", "ticker",
        "open", "high", "low",
        "close", "adj_close", "volume",
    ]
    #Así quito el resto
    for col in expected_cols:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[expected_cols]

    # Guardar dataset limpio
    clean_path = raw_dir / "prices_2019_2025.csv"
    df.to_csv(clean_path, index=False)
    print(f"Dataset guardado en: {clean_path} (filas: {len(df)})")

    # Crear y guardar versión sucia, la usada
    df_dirty = ensuciar_df(df)
    dirty_path = raw_dir / "prices_dirty_2019_2025.csv"
    df_dirty.to_csv(dirty_path, index=False)
    print(f"Dataset sucio guardado en: {dirty_path} (filas: {len(df_dirty)})")



build_prices_dataset()
