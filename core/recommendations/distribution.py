def generate_distribution_recommendations(result: dict) -> list[str]:
    recs = []

    if result["total_loss_pct"] > 12:
        recs.append("Investigate technical and non-technical distribution losses.")

    if result["consumer_voltage_v"] < 215:
        recs.append("Review feeder voltage regulation and transformer tap settings.")

    if result["dt_loading_pct"] > 80:
        recs.append("Review distribution transformer loading and rebalance feeder demand.")

    if result["risk_score"] >= 80:
        recs.append("Urgent field inspection required in the affected distribution zone.")

    if not recs:
        recs.append("Distribution system operating within normal limits.")

    return recs
