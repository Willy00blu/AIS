"""
Elenco tabelle disponibili nel dataset Global Fishing Watch.

Questo script elenca tutte le tabelle pubbliche disponibili nel
dataset gfw_public_data di Global Fishing Watch su BigQuery.

Utile per esplorare quali dati sono accessibili oltre alla tabella
fishing_effort_byvessel_v2.

Uso:
    python lista_tabelle_gfw.py

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

# Dataset pubblico di Global Fishing Watch
DATASET_ID = "global-fishing-watch.gfw_public_data"


# =============================================================================
# FUNZIONI
# =============================================================================

def list_available_tables():
    """
    Elenca tutte le tabelle disponibili nel dataset GFW.
    """
    try:
        client = bigquery.Client.from_service_account_json(str(KEY_PATH))
        tables = client.list_tables(DATASET_ID)

        print(f"\n--- TABELLE IN {DATASET_ID} ---")
        for table in tables:
            print(f"  {table.table_id}")
        print("-------------------------------\n")

    except Exception as e:
        print(f"Errore: {e}")
        raise


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    list_available_tables()
