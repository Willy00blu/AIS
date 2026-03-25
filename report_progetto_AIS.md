# Report — Progetto AIS Stretto di Sicilia

## 1. Architettura del progetto

Il progetto è composto da due moduli principali:

**`script gestione_DB_AIS_processati/`** — dati storici
- Query su BigQuery (Global Fishing Watch) per estrarre dati di pesca aggregati per cella geografica
- Area: lat 35–38.5, lon 10–15.5 (Sicilia)
- Periodi: 2018–2020, campionamento stagionale (gen, apr, lug, ott)
- Colonne: `date`, `mmsi`, `lat`, `lon`, `fishing_hours`

**`aisstream_real_time_AIS_raw/`** — acquisizione real-time
- Connessione WebSocket a aisstream.io
- Bounding box: lat 32.35–39.12, lon 9.50–19.44
- Filtra solo messaggi `PositionReport`
- Salvataggio su CSV con 23 colonne (MMSI, posizione, SOG, COG, heading, ecc.)

---

## 2. Acquisizione real-time

**Prestazioni osservate:**
- Velocità normale: ~0.50 msg/s
- Velocità ridotta: ~0.13 msg/s (variazione legata al traffico navale reale, non al sistema)

**Limite principale — copertura terrestre:**
aisstream.io aggrega ricevitori AIS costieri con portata ~40–60 km dalla costa. In mare aperto il segnale non viene ricevuto.

**Dati acquisiti (10.691 righe):**
- Concentrati vicino a **Palermo** (lat 38.0, lon 12.5)
- Concentrati vicino allo **Stretto di Messina** (lat 38.2, lon 15.2)
- Copertura quasi assente nel **Canale di Sicilia** (mare aperto tra Tunisia e Sicilia)

---

## 3. Dati GFW (Global Fishing Watch)

- Dati **non real-time**, aggregati per celle di griglia
- Ogni punto rappresenta una cella geografica con ore di pesca, non una nave
- Utili per analisi di attività di pesca storica, non per tracking navale live

---

## 4. Visualizzatori sviluppati

**`visualizer.py`** — dati aisstream real-time
- Puntini rossi sulla mappa per ogni posizione ricevuta
- Rettangolo blu con il bounding box di acquisizione
- Auto-refresh ogni 10 secondi
- Avvio: `./run_visualizer.sh`

**`visualizer_db.py`** — dati GFW storici
- Heatmap basata sul numero di navi uniche per cella
- Tag rossi sulle celle con fishing hours intensive
- Slider per regolare la soglia fishing hours
- Selettore periodo (es. `sicilia_2018_01`)
- Avvio: `./run_visualizer_db.sh`

---

## 5. Limite strutturale — AIS terrestre vs satellitare

| | AIS Terrestre (aisstream) | AIS Satellitare |
|---|---|---|
| Copertura | Fino a ~60 km dalla costa | Globale |
| Latenza | Real-time | Real-time o quasi |
| Costo | Gratuito | A pagamento |
| Mare aperto | No | Sì |

**Per coprire il Canale di Sicilia in real-time serve AIS satellitare.** Le opzioni valutate: Spire Maritime, MarineTraffic API, VesselFinder — tutte a pagamento. Non esistono fonti gratuite per il Mediterraneo con copertura satellitare real-time.

---

## 6. Stato attuale e strategia di acquisizione

**Problema:** il dataset aisstream accumulato (10.691 righe) è insufficiente per analisi statisticamente significative. Serve una raccolta prolungata nel tempo.

**Strategie valutate:**

**A — Continuare sulla zona attuale (Sicilia intera)**
- Pro: setup già funzionante, cattura traffico costiero reale
- Contro: bounding box troppo grande per pochi segnali, il Canale di Sicilia aperto rimane scoperto

**B — Restringere il bounding box sulle zone dense**
- Focalizzarsi su Palermo + Stretto di Messina dove i segnali sono effettivamente presenti
- Pro: più messaggi per unità di tempo, dati più densi e utili
- Contro: si perde la visione d'insieme

**C — Acquisizione multi-zona con bounding box multipli**
- aisstream supporta più bounding box nella stessa connessione
- Si potrebbero definire box separati su Palermo, Messina, Porto Empedocle
- Pro: massimizza i segnali catturati nelle zone coperte
- Contro: non risolve il problema del mare aperto

**D — Integrare fonte satellitare per il mare aperto**
- Necessaria per avere copertura completa del Canale di Sicilia
- Richiede budget (MarineTraffic API, Spire Maritime, ecc.)

**E — Cambiare zona di acquisizione** *(opzione in valutazione)*
- Spostare il bounding box su un'area del Mediterraneo con maggiore densità di ricevitori AIS terrestri e traffico più intenso
- Zone candidate da valutare: Stretto di Gibilterra, Canale della Manica, costa ligure/genovese, Porto di Barcellona
- Pro: più dati per unità di tempo, dataset più ricco in meno tempo
- Contro: si perde il focus geografico sulla Sicilia
- Da fare: identificare la zona ottimale confrontando densità di traffico e copertura aisstream

**Raccomandazione attuale:** valutare l'opzione **E** identificando una zona ad alta densità di traffico prima di spostare l'acquisizione. Nel breve termine le opzioni **B o C** restano valide per densificare il dataset esistente sulla Sicilia.
