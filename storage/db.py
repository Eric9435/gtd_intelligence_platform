import sqlite3
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transmission_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        substation_name TEXT,
        transformer_mva REAL,
        load_mw REAL,
        primary_kv REAL,
        secondary_kv REAL,
        current_r REAL,
        current_y REAL,
        current_b REAL,
        power_factor REAL,
        oil_temp REAL,
        winding_temp REAL,
        loading_pct REAL,
        avg_current REAL,
        imbalance_pct REAL,
        voltage_dev_pct REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS generation_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT,
        plant_type TEXT,
        installed_capacity_mw REAL,
        available_capacity_mw REAL,
        actual_generation_mw REAL,
        efficiency_pct REAL,
        reserve_margin_mw REAL,
        utilization_pct REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS distribution_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone_name TEXT,
        feeder_name TEXT,
        feeder_load_mw REAL,
        dt_rating_mva REAL,
        dt_load_mw REAL,
        consumer_voltage_v REAL,
        technical_loss_pct REAL,
        non_technical_loss_pct REAL,
        total_loss_pct REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_transmission_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO transmission_records (
        substation_name,
        transformer_mva,
        load_mw,
        primary_kv,
        secondary_kv,
        current_r,
        current_y,
        current_b,
        power_factor,
        oil_temp,
        winding_temp,
        loading_pct,
        avg_current,
        imbalance_pct,
        voltage_dev_pct,
        risk_score,
        risk_level,
        issues,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["substation_name"],
        record["transformer_mva"],
        record["load_mw"],
        record["primary_kv"],
        record["secondary_kv"],
        record["current_r"],
        record["current_y"],
        record["current_b"],
        record["power_factor"],
        record["oil_temp"],
        record["winding_temp"],
        record["loading_pct"],
        record["avg_current"],
        record["imbalance_pct"],
        record["voltage_dev_pct"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))

    conn.commit()
    conn.close()


def save_generation_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO generation_records (
        plant_name,
        plant_type,
        installed_capacity_mw,
        available_capacity_mw,
        actual_generation_mw,
        efficiency_pct,
        reserve_margin_mw,
        utilization_pct,
        risk_score,
        risk_level,
        issues,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["plant_name"],
        record["plant_type"],
        record["installed_capacity_mw"],
        record["available_capacity_mw"],
        record["actual_generation_mw"],
        record["efficiency_pct"],
        record["reserve_margin_mw"],
        record["utilization_pct"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))

    conn.commit()
    conn.close()


def save_distribution_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO distribution_records (
        zone_name,
        feeder_name,
        feeder_load_mw,
        dt_rating_mva,
        dt_load_mw,
        consumer_voltage_v,
        technical_loss_pct,
        non_technical_loss_pct,
        total_loss_pct,
        risk_score,
        risk_level,
        issues,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["zone_name"],
        record["feeder_name"],
        record["feeder_load_mw"],
        record["dt_rating_mva"],
        record["dt_load_mw"],
        record["consumer_voltage_v"],
        record["technical_loss_pct"],
        record["non_technical_loss_pct"],
        record["total_loss_pct"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))

    conn.commit()
    conn.close()


def fetch_all_transmission_records():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM transmission_records ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_all_generation_records():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM generation_records ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_all_distribution_records():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM distribution_records ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

