"""
Verifica range temporale del dataset Global Fishing Watch.

Questo script interroga il database per determinare:
- Data di inizio copertura dati
- Data di fine copertura dati
- Numero totale di record disponibili

Utile per pianificare le query e capire quali periodi sono disponibili.

Uso:
    python range_temporale.py

Requisiti:
    - File chiave.json valido per autenticazione Google Cloud
    - Pacchetto: google-cloud-bigquery
"""

from google.cloud import bigquery
from pathlib import Path


# =============================================================================
# CONFIGURAZIONE
# =============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
KEY_PATH = PROJECT_ROOT / "chiave.json"

TABLE_ID = "global-fishing-watch.gfw_public_data.fishing_effort_byvessel_v2"


# =============================================================================
# FUNZIONI
# =============================================================================

def check_data_limits():
    """
    Recupera i limiti temporali e la dimensione del dataset.

    Esegue una query aggregata per ottenere data minima, massima
    e conteggio totale dei record.
    """
    query = f"""
        SELECT
            MIN(date) AS data_inizio,
            MAX(date) AS data_fine,
            COUNT(*) AS totale_righe
        FROM
            `{TABLE_ID}`
    """

    try:
        client = bigquery.Client.from_service_account_json(str(KEY_PATH))
        result = client.query(query).to_dataframe()

        print("\n--- LIMITI TEMPORALI DATASET ---")
        print(f"  Prima data disponibile: {result['data_inizio'].iloc[0]}")
        print(f"  Ultima data disponibile: {result['data_fine'].iloc[0]}")
        print(f"  Totale record: {result['totale_righe'].iloc[0]:,}")
        print("--------------------------------\n")

    except Exception as e:
        print(f"Errore: {e}")
        raise


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    check_data_limits()
