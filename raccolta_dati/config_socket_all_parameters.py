import asyncio
import websockets
import json
import time
from datetime import datetime, timedelta
from csv_writer import init_csv, save_to_csv

# Configurazione iniziale
API_KEY = "c58fc690d63cf269c5b497fa9d83fda8a7c6258a"
STRETTO_SICILIA = [[[32.3531186757, 9.5017912796], [39.1207367613, 19.4354646574]]]
START_TIME = time.time()

async def connect_ais_stream():
    init_csv()
    url = "wss://stream.aisstream.io/v0/stream"

    count_ais = 0
    window_start = time.time()
    window_count = 0

    async with websockets.connect(url) as websocket:
        subscribe_msg = {
            "APIKey": API_KEY,
            "BoundingBoxes": STRETTO_SICILIA,
            "FilterMessageTypes": ["PositionReport"]
        }

        await websocket.send(json.dumps(subscribe_msg))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connesso allo Stretto di Sicilia...")

        async for message_json in websocket:
            msg = json.loads(message_json)

            if msg["MessageType"] == "PositionReport":
                # Estrazione dei dati dinamici (PositionReport)
                pos_report = msg["Message"]["PositionReport"]

                cog          = pos_report["Cog"]
                comm_state   = pos_report["CommunicationState"]
                latitude     = pos_report["Latitude"]
                longitude    = pos_report["Longitude"]
                message_id   = pos_report["MessageID"]
                nav_status   = pos_report["NavigationalStatus"]
                pos_accuracy = pos_report["PositionAccuracy"]
                raim         = pos_report["Raim"]
                rot          = pos_report["RateOfTurn"]
                repeat_ind   = pos_report["RepeatIndicator"]
                sog          = pos_report["Sog"]
                spare        = pos_report["Spare"]
                manoeuvre_ind = pos_report["SpecialManoeuvreIndicator"]
                timestamp    = pos_report["Timestamp"]
                heading      = pos_report["TrueHeading"]
                user_id      = pos_report["UserID"]
                is_valid     = pos_report["Valid"]

                # Estrazione del tipo di messaggio
                msg_type = msg["MessageType"]

                # Estrazione dei Metadati
                meta = msg["MetaData"]

                mmsi      = meta["MMSI"]
                ship_name = meta["ShipName"]
                meta_lat  = meta["latitude"]
                meta_lon  = meta["longitude"]
                time_utc  = meta["time_utc"]

                # Salvataggio CSV (tramite csv_writer)
                save_to_csv({
                    "msg_type": msg_type,
                    "mmsi": mmsi, "ship_name": ship_name,
                    "meta_lat": meta_lat, "meta_lon": meta_lon, "time_utc": time_utc,
                    "cog": cog, "comm_state": comm_state,
                    "latitude": latitude, "longitude": longitude,
                    "message_id": message_id, "nav_status": nav_status,
                    "pos_accuracy": pos_accuracy, "raim": raim, "rot": rot,
                    "repeat_ind": repeat_ind, "sog": sog, "spare": spare,
                    "manoeuvre_ind": manoeuvre_ind, "timestamp": timestamp,
                    "heading": heading, "user_id": user_id, "is_valid": is_valid
                })

                # Statistiche
                count_ais += 1
                window_count += 1
                now = time.time()
                elapsed_window = now - window_start

                if elapsed_window >= 1.0:
                    msg_per_sec = count_ais / (time.time() - START_TIME)
                    uptime = str(timedelta(seconds=int(now - START_TIME)))
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Uptime: {uptime} | "
                          f"Totale: {count_ais} msg | "
                          f"Velocità: {msg_per_sec:.2f} msg/s")
                    window_start = now
                    window_count = 0

    return count_ais

if __name__ == "__main__":
    try:
        asyncio.run(connect_ais_stream())
    except KeyboardInterrupt:
        durata = str(timedelta(seconds=int(time.time() - START_TIME)))
        print(f"\nRaccolta interrotta. Durata totale sessione: {durata}")