def calculate_annual_profit(annual_revenue_mmk: float, opex_monthly_mmk: float) -> float:
    return annual_revenue_mmk - (opex_monthly_mmk * 12)


def calculate_roi_pct(capex_mmk: float, annual_profit_mmk: float) -> float:
    if capex_mmk <= 0:
        return 0.0
    return (annual_profit_mmk / capex_mmk) * 100.0


def calculate_payback_years(capex_mmk: float, annual_profit_mmk: float) -> float:
    if annual_profit_mmk <= 0:
        return 0.0
    return capex_mmk / annual_profit_mmk
