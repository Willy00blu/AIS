import subprocess
import time
import sys

# Inserisci qui il nome esatto del tuo file principale
SCRIPT_AIS = "raccolta_dati/config_socket_all_parameters.py"

def main():
    print(f"[WATCHDOG] Inizializzazione monitoraggio per: {SCRIPT_AIS}")
    
    while True:
        print(f"\n[WATCHDOG] ---> Avvio processo alle {time.strftime('%H:%M:%S')}")
        
        try:
            # Esecuzione con flag -u per forzare la stampa dei log in tempo reale
            processo = subprocess.run([sys.executable, "-u", SCRIPT_AIS])
            
            # IL FIX: A prescindere da come è terminato (errore di rete o timeout pulito), noi lo facciamo ripartire.
            print(f"[WATCHDOG] Processo terminato (Exit Code: {processo.returncode}).")
            print("[WATCHDOG] Riavvio automatico tra 5 secondi...")
            time.sleep(5)
                
        except KeyboardInterrupt:
            # L'UNICO MODO PER FERMARLO: Premere CTRL+C nel terminale
            print("\n[WATCHDOG] Interruzione manuale rilevata. Spegnimento definitivo del sistema.")
            break
        except Exception as e:
            print(f"[WATCHDOG] Errore di sistema nel controllore: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()