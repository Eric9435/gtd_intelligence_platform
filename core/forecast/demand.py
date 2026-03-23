def forecast_next_demand(current_demand_mw: float, growth_pct: float, periods: int = 6) -> list[dict]:
    results = []
    demand = current_demand_mw

    for period in range(1, periods + 1):
        demand = demand * (1 + growth_pct / 100.0)
        results.append({
            "period": f"Month {period}",
            "forecast_demand_mw": round(demand, 2),
        })

    return results
