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
        dt_loading_pct REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone_name TEXT,
        units_sold_mwh REAL,
        tariff_mmk_per_kwh REAL,
        revenue_mmk REAL,
        industrial_pct REAL,
        residential_pct REAL,
        commercial_pct REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS roi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        capex_mmk REAL,
        opex_monthly_mmk REAL,
        annual_revenue_mmk REAL,
        annual_profit_mmk REAL,
        roi_pct REAL,
        payback_years REAL,
        risk_score REAL,
        risk_level TEXT,
        issues TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS export_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone_name TEXT,
        total_generation_mw REAL,
        total_demand_mw REAL,
        surplus_mw REAL,
        export_hours REAL,
        export_tariff_mmk_per_kwh REAL,
        export_energy_mwh REAL,
        export_revenue_mmk REAL,
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
        substation_name, transformer_mva, load_mw, primary_kv, secondary_kv,
        current_r, current_y, current_b, power_factor, oil_temp, winding_temp,
        loading_pct, avg_current, imbalance_pct, voltage_dev_pct,
        risk_score, risk_level, issues, created_at
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
        plant_name, plant_type, installed_capacity_mw, available_capacity_mw,
        actual_generation_mw, efficiency_pct, reserve_margin_mw,
        utilization_pct, risk_score, risk_level, issues, created_at
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
        zone_name, feeder_name, feeder_load_mw, dt_rating_mva, dt_load_mw,
        consumer_voltage_v, technical_loss_pct, non_technical_loss_pct,
        total_loss_pct, dt_loading_pct, risk_score, risk_level, issues, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        record["dt_loading_pct"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))
    conn.commit()
    conn.close()


def save_sales_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO sales_records (
        zone_name, units_sold_mwh, tariff_mmk_per_kwh, revenue_mmk,
        industrial_pct, residential_pct, commercial_pct,
        risk_score, risk_level, issues, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["zone_name"],
        record["units_sold_mwh"],
        record["tariff_mmk_per_kwh"],
        record["revenue_mmk"],
        record["industrial_pct"],
        record["residential_pct"],
        record["commercial_pct"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))
    conn.commit()
    conn.close()


def save_roi_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO roi_records (
        project_name, capex_mmk, opex_monthly_mmk, annual_revenue_mmk,
        annual_profit_mmk, roi_pct, payback_years,
        risk_score, risk_level, issues, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["project_name"],
        record["capex_mmk"],
        record["opex_monthly_mmk"],
        record["annual_revenue_mmk"],
        record["annual_profit_mmk"],
        record["roi_pct"],
        record["payback_years"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))
    conn.commit()
    conn.close()


def save_export_record(record: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO export_records (
        zone_name, total_generation_mw, total_demand_mw, surplus_mw,
        export_hours, export_tariff_mmk_per_kwh, export_energy_mwh,
        export_revenue_mmk, risk_score, risk_level, issues, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["zone_name"],
        record["total_generation_mw"],
        record["total_demand_mw"],
        record["surplus_mw"],
        record["export_hours"],
        record["export_tariff_mmk_per_kwh"],
        record["export_energy_mwh"],
        record["export_revenue_mmk"],
        record["risk_score"],
        record["risk_level"],
        record["issues"],
        record["created_at"],
    ))
    conn.commit()
    conn.close()


def _fetch_all(table_name: str):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_all_transmission_records():
    return _fetch_all("transmission_records")


def fetch_all_generation_records():
    return _fetch_all("generation_records")


def fetch_all_distribution_records():
    return _fetch_all("distribution_records")


def fetch_all_sales_records():
    return _fetch_all("sales_records")


def fetch_all_roi_records():
    return _fetch_all("roi_records")


def fetch_all_export_records():
    return _fetch_all("export_records")

