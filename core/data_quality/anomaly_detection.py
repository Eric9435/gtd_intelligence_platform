def detect_transmission_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("oil_temp", 0) > 110:
        anomalies.append("Oil temperature is unusually high.")
    if inputs.get("winding_temp", 0) > 130:
        anomalies.append("Winding temperature is unusually high.")
    if max(inputs.get("current_r", 0), inputs.get("current_y", 0), inputs.get("current_b", 0)) > 5000:
        anomalies.append("Phase current appears unusually high.")
    if inputs.get("load_mw", 0) > 10000:
        anomalies.append("Load appears unusually high.")

    return anomalies


def detect_generation_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("actual_generation_mw", 0) > inputs.get("installed_capacity_mw", 0):
        anomalies.append("Actual generation exceeds installed capacity.")
    if inputs.get("available_capacity_mw", 0) > inputs.get("installed_capacity_mw", 0):
        anomalies.append("Available capacity exceeds installed capacity.")

    return anomalies


def detect_distribution_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("consumer_voltage_v", 0) > 260:
        anomalies.append("Consumer voltage appears unusually high.")
    if inputs.get("technical_loss_pct", 0) > 50:
        anomalies.append("Technical loss appears unusually high.")
    if inputs.get("non_technical_loss_pct", 0) > 50:
        anomalies.append("Non-technical loss appears unusually high.")

    return anomalies


def detect_sales_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("tariff_mmk_per_kwh", 0) > 10000:
        anomalies.append("Tariff appears unusually high.")
    if inputs.get("units_sold_mwh", 0) > 100000000:
        anomalies.append("Units sold appears unusually high.")

    return anomalies


def detect_roi_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("capex_mmk", 0) <= 0:
        anomalies.append("CAPEX must be greater than zero.")
    if inputs.get("annual_revenue_mmk", 0) < 0:
        anomalies.append("Annual revenue cannot be negative.")

    return anomalies


def detect_export_anomalies(inputs: dict) -> list[str]:
    anomalies = []

    if inputs.get("export_hours", 0) > 24:
        anomalies.append("Export hours cannot exceed 24 per day.")
    if inputs.get("total_generation_mw", 0) < 0 or inputs.get("total_demand_mw", 0) < 0:
        anomalies.append("Generation and demand must be non-negative.")

    return anomalies
