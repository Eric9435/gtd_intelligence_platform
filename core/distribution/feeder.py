def calculate_total_loss_pct(technical_loss_pct: float, non_technical_loss_pct: float) -> float:
    return technical_loss_pct + non_technical_loss_pct


def calculate_dt_loading_pct(dt_load_mw: float, dt_rating_mva: float, assumed_pf: float = 0.9) -> float:
    if dt_rating_mva <= 0 or assumed_pf <= 0:
        return 0.0
    return (dt_load_mw / (dt_rating_mva * assumed_pf)) * 100.0
