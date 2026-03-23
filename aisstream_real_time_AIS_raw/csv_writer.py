import csv
import os

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ais_data_raw_rt.csv")

CSV_COLUMNS = [
    "msg_type",
    "mmsi", "ship_name", "meta_lat", "meta_lon", "time_utc",
    "cog", "comm_state", "latitude", "longitude", "message_id",
    "nav_status", "pos_accuracy", "raim", "rot", "repeat_ind",
    "sog", "spare", "manoeuvre_ind", "timestamp", "heading",
    "user_id", "is_valid"
]

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()

def save_to_csv(row: dict):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writerow(row)
