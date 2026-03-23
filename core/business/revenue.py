
def calculate_revenue_mmk(units_sold_mwh: float, tariff_mmk_per_kwh: float) -> float:
    return units_sold_mwh * 1000 * tariff_mmk_per_kwh
