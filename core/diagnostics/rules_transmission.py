from config import (
    WARNING_LOADING_PCT,
    CRITICAL_LOADING_PCT,
    WARNING_TEMP_C,
    CRITICAL_TEMP_C,
)


def evaluate_transmission_issues(
    loading_pct: float,
    oil_temp: float,
    winding_temp: float,
    imbalance_pct: float,
    voltage_dev_pct: float,
    power_factor: float,
) -> list[str]:
    issues = []

    if loading_pct >= CRITICAL_LOADING_PCT:
        issues.append("Transformer overload condition detected.")
    elif loading_pct >= WARNING_LOADING_PCT:
        issues.append("Transformer loading is high.")

    hottest_temp = max(oil_temp, winding_temp)
    if hottest_temp >= CRITICAL_TEMP_C:
        issues.append("Critical transformer thermal stress detected.")
    elif hottest_temp >= WARNING_TEMP_C:
        issues.append("Transformer temperature is above recommended range.")

    if imbalance_pct >= 15:
        issues.append("Severe phase current imbalance detected.")
    elif imbalance_pct >= 8:
        issues.append("Moderate phase current imbalance detected.")

    if voltage_dev_pct >= 10:
        issues.append("Critical voltage deviation detected.")
    elif voltage_dev_pct >= 5:
        issues.append("Voltage deviation is above preferred limit.")

    if power_factor < 0.8:
        issues.append("Power factor is critically low.")
    elif power_factor < 0.9:
        issues.append("Power factor is below target.")

    return issues
