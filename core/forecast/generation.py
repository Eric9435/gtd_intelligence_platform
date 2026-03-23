def forecast_next_generation(current_generation_mw: float, derating_pct: float, periods: int = 6) -> list[dict]:
    results = []
    generation = current_generation_mw

    for period in range(1, periods + 1):
        generation = generation * (1 - derating_pct / 100.0)
        results.append({
            "period": f"Month {period}",
            "forecast_generation_mw": round(generation, 2),
        })

    return results
