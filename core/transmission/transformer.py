def calculate_loading_pct(load_mw: float, transformer_mva: float, power_factor: float) -> float:
    if transformer_mva <= 0 or power_factor <= 0:
        return 0.0
    return (load_mw / (transformer_mva * power_factor)) * 100.0


def calculate_average_current(current_r: float, current_y: float, current_b: float) -> float:
    return (current_r + current_y + current_b) / 3.0


def calculate_phase_imbalance_pct(current_r: float, current_y: float, current_b: float) -> float:
    avg = calculate_average_current(current_r, current_y, current_b)
    if avg <= 0:
        return 0.0

    max_dev = max(
        abs(current_r - avg),
        abs(current_y - avg),
        abs(current_b - avg),
    )
    return (max_dev / avg) * 100.0


def calculate_voltage_deviation_pct(nominal_kv: float, actual_kv: float) -> float:
    if nominal_kv <= 0:
        return 0.0
    return ((nominal_kv - actual_kv) / nominal_kv) * 100.0
