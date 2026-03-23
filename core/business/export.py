def calculate_surplus_mw(total_generation_mw: float, total_demand_mw: float) -> float:
    return total_generation_mw - total_demand_mw


def calculate_export_energy_mwh(surplus_mw: float, export_hours: float) -> float:
    if surplus_mw <= 0 or export_hours <= 0:
        return 0.0
    return surplus_mw * export_hours


def calculate_export_revenue_mmk(export_energy_mwh: float, export_tariff_mmk_per_kwh: float) -> float:
    return export_energy_mwh * 1000 * export_tariff_mmk_per_kwh
