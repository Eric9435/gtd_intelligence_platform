def generate_generation_recommendations(result: dict) -> list[str]:
    recs = []

    if result["utilization_pct"] > 95:
        recs.append("Increase available spinning reserve or reduce generation stress.")
    elif result["utilization_pct"] > 80:
        recs.append("Monitor plant utilization closely during peak demand.")

    if result["efficiency_pct"] < 85:
        recs.append("Inspect plant efficiency drivers and review operating losses.")

    if result["reserve_margin_mw"] < 20:
        recs.append("Improve reserve planning to reduce generation adequacy risk.")

    if result["risk_score"] >= 80:
        recs.append("Urgent engineering review required for plant operation strategy.")

    if not recs:
        recs.append("Generation system operating within normal limits.")

    return recs
