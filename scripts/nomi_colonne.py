"""
Ispezione schema tabella Global Fishing Watch.

Questo script mostra tutte le colonne disponibili nella tabella
fishing_effort_byvessel_v2, utile per capire quali campi sono
disponibili prima di costruire le query.

Uso:
    python nomi_colonne.py

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

# Tabella da ispezionare
TABLE_ID = "global-fishing-watch.gfw_public_data.fishing_effort_byvessel_v2"


# =============================================================================
# FUNZIONI
# =============================================================================

def inspect_table_schema():
    """
    Recupera e stampa lo schema della tabella BigQuery.

    Mostra nome e tipo di ogni colonna disponibile.
    """
    try:
        client = bigquery.Client.from_service_account_json(str(KEY_PATH))
        table = client.get_table(TABLE_ID)

        print(f"\nConnessione riuscita: {TABLE_ID}")
        print("\n--- COLONNE DISPONIBILI ---")
        for field in table.schema:
            print(f"  {field.name:<25} {field.field_type}")
        print("---------------------------\n")

    except Exception as e:
        print(f"Errore durante l'ispezione: {e}")
        raise


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    inspect_table_schema()
