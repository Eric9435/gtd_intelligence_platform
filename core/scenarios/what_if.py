def run_what_if_scenario(
    base_generation_mw: float,
    base_demand_mw: float,
    generation_change_pct: float = 0.0,
    demand_change_pct: float = 0.0,
    loss_pct: float = 0.0,
):
    new_generation = base_generation_mw * (1 + generation_change_pct / 100.0)
    new_demand = base_demand_mw * (1 + demand_change_pct / 100.0)

    available_after_loss = new_generation * (1 - loss_pct / 100.0)
    surplus_deficit_mw = available_after_loss - new_demand

    if surplus_deficit_mw > 0:
        status = "SURPLUS"
        risk = "NORMAL"
    elif surplus_deficit_mw == 0:
        status = "BALANCED"
        risk = "WARNING"
    else:
        status = "DEFICIT"
        risk = "HIGH"

    return {
        "base_generation_mw": round(base_generation_mw, 2),
        "base_demand_mw": round(base_demand_mw, 2),
        "generation_change_pct": generation_change_pct,
        "demand_change_pct": demand_change_pct,
        "loss_pct": loss_pct,
        "new_generation_mw": round(new_generation, 2),
        "available_after_loss_mw": round(available_after_loss, 2),
        "new_demand_mw": round(new_demand, 2),
        "surplus_deficit_mw": round(surplus_deficit_mw, 2),
        "status": status,
        "risk_level": risk,
    }
