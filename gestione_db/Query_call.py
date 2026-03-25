"""
Query BigQuery per estrarre dati AIS da Global Fishing Watch.

Questo script esegue un campionamento stratificato dei dati di pesca
nell'area della Sicilia, estraendo un mese rappresentativo per ogni
stagione (Gennaio, Aprile, Luglio, Ottobre) su più anni.

Dataset utilizzato:
    global-fishing-watch.gfw_public_data.fishing_effort_byvessel_v2

Output:
    File CSV nella cartella ../dataset_AIS/ con naming convention:
    sicilia_YYYY_MM.csv

Requisiti:
    - File chiave.json valido per autenticazione Google Cloud
    - Pacchetti: google-cloud-bigquery, pandas
"""

import os
import calendar
import pandas as pd
from google.cloud import bigquery
from pathlib import Path


# =============================================================================
# CONFIGURAZIONE
# =============================================================================

# Percorso alla chiave di servizio Google Cloud (relativo alla root del progetto)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
KEY_PATH = PROJECT_ROOT / "chiave.json"

# Directory di output per i file CSV
OUTPUT_DIR = PROJECT_ROOT / "dataset_AIS"

# Area geografica: Sicilia e mare circostante
BOUNDING_BOX = {
    "lat_min": 35.0,
    "lat_max": 38.5,
    "lon_min": 10.0,
    "lon_max": 15.5,
}

# Parametri di campionamento stratificato
YEARS = [2018, 2019, 2020]
MONTHS = [1, 4, 7, 10]  # Un mese per stagione


# =============================================================================
# FUNZIONI
# =============================================================================

def build_query(start_date: str, end_date: str) -> str:
    """
    Costruisce la query SQL per estrarre i dati di pesca.

    Args:
        start_date: Data inizio periodo (formato YYYY-MM-DD)
        end_date: Data fine periodo (formato YYYY-MM-DD)

    Returns:
        Query SQL come stringa
    """
    return f"""
        SELECT
            date,
            mmsi,
            cell_ll_lat AS lat,
            cell_ll_lon AS lon,
            fishing_hours
        FROM
            `global-fishing-watch.gfw_public_data.fishing_effort_byvessel_v2`
        WHERE
            date BETWEEN '{start_date}' AND '{end_date}'
            AND cell_ll_lat BETWEEN {BOUNDING_BOX['lat_min']} AND {BOUNDING_BOX['lat_max']}
            AND cell_ll_lon BETWEEN {BOUNDING_BOX['lon_min']} AND {BOUNDING_BOX['lon_max']}
        ORDER BY date DESC
    """


def fetch_stratified_data():
    """
    Estrae dati AIS stratificati per anno e stagione dall'API BigQuery.

    Salva un file CSV per ogni combinazione anno/mese nella directory di output.
    """
    # Crea la directory di output se non esiste
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        client = bigquery.Client.from_service_account_json(str(KEY_PATH))
        print("Autorizzazione OK. Avvio estrazione stratificata...\n")

        for year in YEARS:
            for month in MONTHS:
                # Calcolo dinamico dell'ultimo giorno del mese
                _, last_day = calendar.monthrange(year, month)

                start_date = f"{year}-{month:02d}-01"
                end_date = f"{year}-{month:02d}-{last_day:02d}"

                filename = OUTPUT_DIR / f"sicilia_{year}_{month:02d}.csv"

                print(f"Interrogazione: {start_date} -> {end_date} ...")

                query = build_query(start_date, end_date)
                df = client.query(query).to_dataframe()

                if not df.empty:
                    df.to_csv(filename, index=False)
                    print(f"  Salvato: {filename.name} ({len(df)} righe)")
                else:
                    print(f"  Nessun dato trovato per {year}-{month:02d}")

        print("\nEstrazione completata.")

    except Exception as e:
        print(f"\nErrore durante l'estrazione: {e}")
        raise


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    fetch_stratified_data()
