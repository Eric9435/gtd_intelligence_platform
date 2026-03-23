def calculate_utilization_pct(actual_generation_mw: float, available_capacity_mw: float) -> float:
    if available_capacity_mw <= 0:
        return 0.0
    return (actual_generation_mw / available_capacity_mw) * 100.0


def calculate_reserve_margin_mw(available_capacity_mw: float, actual_generation_mw: float) -> float:
    return available_capacity_mw - actual_generation_mw
