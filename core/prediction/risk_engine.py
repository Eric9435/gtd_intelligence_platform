from config import (
    WARNING_LOADING_PCT,
    CRITICAL_LOADING_PCT,
    WARNING_TEMP_C,
    CRITICAL_TEMP_C,
)


def calculate_risk_score(
    loading_pct: float,
    oil_temp: float,
    winding_temp: float,
    imbalance_pct: float,
    voltage_dev_pct: float,
    power_factor: float,
) -> float:
    score = 0.0

    if loading_pct >= CRITICAL_LOADING_PCT:
        score += 30
    elif loading_pct >= WARNING_LOADING_PCT:
        score += 18

    hottest_temp = max(oil_temp, winding_temp)

    if hottest_temp >= CRITICAL_TEMP_C:
        score += 25
    elif hottest_temp >= WARNING_TEMP_C:
        score += 15

    if imbalance_pct >= 15:
        score += 20
    elif imbalance_pct >= 8:
        score += 10

    if voltage_dev_pct >= 10:
        score += 15
    elif voltage_dev_pct >= 5:
        score += 8

    if power_factor < 0.8:
        score += 10
    elif power_factor < 0.9:
        score += 5

    return min(score, 100.0)


def calculate_generation_risk(utilization_pct: float, efficiency_pct: float, reserve_margin_mw: float) -> float:
    score = 0.0

    if utilization_pct > 95:
        score += 35
    elif utilization_pct > 80:
        score += 20

    if efficiency_pct < 70:
        score += 30
    elif efficiency_pct < 85:
        score += 15

    if reserve_margin_mw < 0:
        score += 30
    elif reserve_margin_mw < 20:
        score += 15

    return min(score, 100.0)


def calculate_distribution_risk(total_loss_pct: float, consumer_voltage_v: float, dt_loading_pct: float) -> float:
    score = 0.0

    if total_loss_pct > 20:
        score += 35
    elif total_loss_pct > 12:
        score += 20

    if consumer_voltage_v < 200:
        score += 25
    elif consumer_voltage_v < 215:
        score += 12

    if dt_loading_pct > 100:
        score += 25
    elif dt_loading_pct > 80:
        score += 15

    return min(score, 100.0)


def classify_risk_level(score: float) -> str:
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "WARNING"
    return "NORMAL"
