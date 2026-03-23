def generate_executive_insight(snapshot: dict) -> list[str]:
    insights = []

    generation = snapshot.get("generation", {})
    transmission = snapshot.get("transmission", {})
    distribution = snapshot.get("distribution", {})
    sales = snapshot.get("sales", {})
    roi = snapshot.get("roi", {})
    export = snapshot.get("export", {})

    gen_mw = float(generation.get("actual_generation_mw", 0))
    tx_risk = float(transmission.get("risk_score", 0))
    dist_loss = float(distribution.get("total_loss_pct", 0))
    revenue = float(sales.get("revenue_mmk", 0))
    roi_pct = float(roi.get("roi_pct", 0))
    surplus = float(export.get("surplus_mw", 0))
    export_revenue = float(export.get("export_revenue_mmk", 0))

    if gen_mw > 0:
        insights.append(f"Current generation output is {gen_mw:.2f} MW.")

    if tx_risk >= 80:
        insights.append("Transmission risk is critical and needs urgent intervention.")
    elif tx_risk >= 60:
        insights.append("Transmission risk is high and should be prioritized.")
    elif tx_risk >= 30:
        insights.append("Transmission risk is moderate and should be monitored.")

    if dist_loss > 20:
        insights.append("Distribution loss is critically high and may require immediate corrective action.")
    elif dist_loss > 12:
        insights.append("Distribution loss is above target and should be reduced.")

    if revenue > 0:
        insights.append(f"Recorded revenue is {revenue:,.0f} MMK.")

    if roi_pct > 0:
        if roi_pct < 5:
            insights.append("ROI is weak and project economics should be reviewed.")
        elif roi_pct < 12:
            insights.append("ROI is moderate but can be improved.")
        else:
            insights.append("ROI is in a healthy range.")

    if surplus > 0:
        insights.append(f"System surplus is {surplus:.2f} MW and may support export or reserve planning.")

    if export_revenue > 0:
        insights.append(f"Potential export revenue is {export_revenue:,.0f} MMK.")

    if not insights:
        insights.append("No major strategic insight is available from the current snapshot.")

    return insights


def generate_auto_summary_paragraph(snapshot: dict) -> str:
    generation = snapshot.get("generation", {})
    transmission = snapshot.get("transmission", {})
    distribution = snapshot.get("distribution", {})
    sales = snapshot.get("sales", {})
    roi = snapshot.get("roi", {})
    export = snapshot.get("export", {})

    text = (
        f"The latest GT&D snapshot indicates generation at {generation.get('actual_generation_mw', 0)} MW, "
        f"transmission risk score at {transmission.get('risk_score', 0)}, "
        f"distribution loss at {distribution.get('total_loss_pct', 0)} %, "
        f"revenue at {sales.get('revenue_mmk', 0):,.0f} MMK, "
        f"ROI at {roi.get('roi_pct', 0)} %, "
        f"and surplus/export capacity at {export.get('surplus_mw', 0)} MW."
    )
    return text
