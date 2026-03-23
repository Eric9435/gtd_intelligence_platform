def generate_executive_insight(snapshot: dict) -> list[str]:
    insights = []

    generation = snapshot.get("generation", {})
    transmission = snapshot.get("transmission", {})
    distribution = snapshot.get("distribution", {})
    sales = snapshot.get("sales", {})
    roi = snapshot.get("roi", {})
    export = snapshot.get("export", {})

    # Generation
    actual_generation = float(generation.get("actual_generation_mw", 0))
    utilization = float(generation.get("utilization_pct", 0))
    reserve_margin = float(generation.get("reserve_margin_mw", 0))
    efficiency = float(generation.get("efficiency_pct", 0))
    generation_risk = str(generation.get("risk_level", "NORMAL"))

    if actual_generation > 0:
        insights.append(f"Current generation output is {actual_generation:.2f} MW.")

    if utilization > 95:
        insights.append(f"Generation utilization is critically high at {utilization:.1f}%, indicating limited spare capacity.")
    elif utilization > 80:
        insights.append(f"Generation utilization is high at {utilization:.1f}%, requiring close monitoring.")

    if reserve_margin < 0:
        insights.append(f"Generation deficit detected at {reserve_margin:.2f} MW, indicating insufficient available capacity.")
    elif reserve_margin < 20 and actual_generation > 0:
        insights.append(f"Reserve margin is low at {reserve_margin:.2f} MW, reducing operating flexibility.")

    if efficiency > 0 and efficiency < 70:
        insights.append(f"Plant efficiency is critically low at {efficiency:.1f}%, suggesting major performance losses.")
    elif efficiency > 0 and efficiency < 85:
        insights.append(f"Plant efficiency is below target at {efficiency:.1f}%.")

    if generation_risk in ["HIGH", "CRITICAL"]:
        insights.append(f"Generation risk level is {generation_risk.lower()}, requiring operational attention.")

    # Transmission
    loading = float(transmission.get("loading_pct", 0))
    imbalance = float(transmission.get("imbalance_pct", 0))
    voltage_dev = float(transmission.get("voltage_dev_pct", 0))
    tx_risk_score = float(transmission.get("risk_score", 0))
    tx_risk = str(transmission.get("risk_level", "NORMAL"))

    if loading > 100:
        insights.append(f"Transformer loading is overloaded at {loading:.1f}%, exceeding safe operating limits.")
    elif loading > 75:
        insights.append(f"Transformer loading is high at {loading:.1f}%, nearing operational limits.")

    if imbalance > 10:
        insights.append(f"Phase imbalance is significant at {imbalance:.2f}%, which may stress equipment and reduce efficiency.")
    elif imbalance > 3:
        insights.append(f"Phase imbalance detected at {imbalance:.2f}%, which may impact efficiency.")

    if voltage_dev > 8:
        insights.append(f"Voltage deviation is high at {voltage_dev:.2f}%, indicating possible feeder, regulation, or load issues.")
    elif voltage_dev > 4:
        insights.append(f"Voltage deviation is {voltage_dev:.2f}%, indicating possible feeder or load issues.")

    if tx_risk_score > 50 or tx_risk in ["HIGH", "CRITICAL"]:
        insights.append("Transmission risk level is elevated and requires closer monitoring or corrective action.")

    # Distribution
    total_loss = float(distribution.get("total_loss_pct", 0))
    dt_loading = float(distribution.get("dt_loading_pct", 0))
    consumer_voltage = float(distribution.get("consumer_voltage_v", 0))
    dist_risk = str(distribution.get("risk_level", "NORMAL"))

    if total_loss > 20:
        insights.append(f"Distribution loss is critically high at {total_loss:.2f}%, indicating major technical or non-technical loss.")
    elif total_loss > 12:
        insights.append(f"Distribution loss is above target at {total_loss:.2f}%.")

    if dt_loading > 100:
        insights.append(f"Distribution transformer loading is overloaded at {dt_loading:.1f}%.")
    elif dt_loading > 80:
        insights.append(f"Distribution transformer loading is high at {dt_loading:.1f}%.")

    if 0 < consumer_voltage < 200:
        insights.append(f"Consumer voltage is critically low at {consumer_voltage:.1f} V, which may affect service quality.")
    elif 0 < consumer_voltage < 215:
        insights.append(f"Consumer voltage is below preferred level at {consumer_voltage:.1f} V.")

    if dist_risk in ["HIGH", "CRITICAL"]:
        insights.append(f"Distribution risk is {dist_risk.lower()}, indicating weak downstream network performance.")

    # Sales
    revenue = float(sales.get("revenue_mmk", 0))
    units_sold = float(sales.get("units_sold_mwh", 0))
    sales_risk = str(sales.get("risk_level", "NORMAL"))

    if units_sold > 0:
        insights.append(f"Recorded energy sales are {units_sold:.2f} MWh.")

    if revenue > 0:
        insights.append(f"Recorded revenue is {revenue:,.0f} MMK.")

    if sales_risk in ["HIGH", "CRITICAL"]:
        insights.append("Sales data quality or commercial structure requires review.")

    # ROI
    roi_pct = float(roi.get("roi_pct", 0))
    annual_profit = float(roi.get("annual_profit_mmk", 0))
    payback_years = float(roi.get("payback_years", 0))
    roi_risk = str(roi.get("risk_level", "NORMAL"))

    if annual_profit < 0:
        insights.append(f"Annual profit is negative at {annual_profit:,.0f} MMK, indicating financial underperformance.")
    elif annual_profit > 0:
        insights.append(f"Annual profit is estimated at {annual_profit:,.0f} MMK.")

    if roi_pct > 0 and roi_pct < 5:
        insights.append(f"ROI is low at {roi_pct:.2f}%, which may weaken project attractiveness.")
    elif roi_pct >= 12:
        insights.append(f"ROI is healthy at {roi_pct:.2f}%.")

    if payback_years > 10:
        insights.append(f"Payback period is long at {payback_years:.2f} years.")
    elif 0 < payback_years <= 5:
        insights.append(f"Payback period is favorable at {payback_years:.2f} years.")

    if roi_risk in ["HIGH", "CRITICAL"]:
        insights.append("Financial performance risk is elevated and requires strategic review.")

    # Export
    surplus = float(export.get("surplus_mw", 0))
    export_revenue = float(export.get("export_revenue_mmk", 0))
    export_energy = float(export.get("export_energy_mwh", 0))
    export_risk = str(export.get("risk_level", "NORMAL"))

    if surplus > 0:
        insights.append(f"System surplus is {surplus:.2f} MW, creating export or reserve opportunity.")
    elif surplus < 0:
        insights.append(f"System deficit is {abs(surplus):.2f} MW, limiting export capability.")

    if export_energy > 0:
        insights.append(f"Potential export energy is {export_energy:.2f} MWh.")

    if export_revenue > 0:
        insights.append(f"Potential export revenue is {export_revenue:,.0f} MMK.")

    if export_risk in ["HIGH", "CRITICAL"]:
        insights.append("Export feasibility is constrained by current system balance or reserve limitations.")

    if not insights:
        insights.append("System is operating within normal parameters with no significant issues.")

    return insights


def generate_auto_summary_paragraph(snapshot: dict) -> str:
    generation = snapshot.get("generation", {})
    transmission = snapshot.get("transmission", {})
    distribution = snapshot.get("distribution", {})
    sales = snapshot.get("sales", {})
    roi = snapshot.get("roi", {})
    export = snapshot.get("export", {})

    return (
        f"The latest GT&D snapshot indicates generation at {generation.get('actual_generation_mw', 0)} MW, "
        f"transmission risk score at {transmission.get('risk_score', 0)}, "
        f"distribution loss at {distribution.get('total_loss_pct', 0)} %, "
        f"revenue at {sales.get('revenue_mmk', 0):,.0f} MMK, "
        f"ROI at {roi.get('roi_pct', 0)} %, "
        f"and surplus/export capacity at {export.get('surplus_mw', 0)} MW."
    )

