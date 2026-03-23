def generate_business_recommendations(context: dict) -> list[str]:
    recs = []

    revenue = float(context.get("revenue_mmk", 0))
    roi = float(context.get("roi_pct", 0))
    surplus = float(context.get("surplus_mw", 0))
    export_revenue = float(context.get("export_revenue_mmk", 0))
    annual_profit = float(context.get("annual_profit_mmk", 0))
    payback_years = float(context.get("payback_years", 0))

    if revenue > 0 and revenue < 5_000_000_000:
        recs.append("Revenue base is still limited; consider tariff optimization or higher unit sales.")
    if roi > 0 and roi < 12:
        recs.append("ROI is modest; review CAPEX efficiency and annual revenue improvement strategy.")
    if annual_profit <= 0:
        recs.append("Annual profit is weak or negative; review OPEX and financial structure urgently.")
    if payback_years > 5:
        recs.append("Long payback period detected; improve margin or reduce project cost burden.")
    if surplus > 0:
        recs.append("Surplus power exists; evaluate export contracts or internal industrial sales opportunity.")
    if export_revenue > 0:
        recs.append("Export revenue potential detected; model long-term export tariff scenarios.")

    if not recs:
        recs.append("Business indicators are in healthy range. Continue monitoring revenue, ROI, and export margins.")

    return recs
