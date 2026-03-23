def generate_recommendations(result: dict) -> list[str]:
    recs = []

    if result["loading_pct"] > 80:
        recs.append("Reduce transformer loading or redistribute load.")

    if result["imbalance_pct"] > 10:
        recs.append("Balance phase currents to reduce transformer stress.")

    if result["oil_temp"] > 75:
        recs.append("Inspect transformer oil cooling condition.")

    if result["winding_temp"] > 80:
        recs.append("Inspect winding insulation and thermal loading condition.")

    if result["power_factor"] < 0.9:
        recs.append("Improve power factor using capacitor bank or compensation.")

    if abs(result["voltage_dev_pct"]) > 5:
        recs.append("Check voltage regulation and tap changer settings.")

    if result["risk_score"] >= 80:
        recs.append("Urgent engineering inspection required due to critical risk level.")

    if not recs:
        recs.append("System is operating within normal engineering limits.")

    return recs
