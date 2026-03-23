from datetime import datetime

from core.transmission.transformer import (
    calculate_loading_pct,
    calculate_average_current,
    calculate_phase_imbalance_pct,
    calculate_voltage_deviation_pct,
)
from core.generation.capacity import (
    calculate_utilization_pct,
    calculate_reserve_margin_mw,
)
from core.distribution.feeder import (
    calculate_total_loss_pct,
    calculate_dt_loading_pct,
)
from core.business.revenue import calculate_revenue_mmk
from core.business.roi import (
    calculate_annual_profit,
    calculate_roi_pct,
    calculate_payback_years,
)
from core.business.export import (
    calculate_surplus_mw,
    calculate_export_energy_mwh,
    calculate_export_revenue_mmk,
)
from core.prediction.risk_engine import (
    calculate_risk_score,
    calculate_generation_risk,
    calculate_distribution_risk,
    classify_risk_level,
)
from core.diagnostics.rules_transmission import evaluate_transmission_issues


def analyze_transmission_input(inputs: dict) -> dict:
    loading_pct = calculate_loading_pct(
        load_mw=inputs["load_mw"],
        transformer_mva=inputs["transformer_mva"],
        power_factor=inputs["power_factor"],
    )

    avg_current = calculate_average_current(
        inputs["current_r"],
        inputs["current_y"],
        inputs["current_b"],
    )

    imbalance_pct = calculate_phase_imbalance_pct(
        inputs["current_r"],
        inputs["current_y"],
        inputs["current_b"],
    )

    voltage_dev_pct = calculate_voltage_deviation_pct(
        nominal_kv=inputs["primary_kv"],
        actual_kv=inputs["secondary_kv"],
    )

    risk_score = calculate_risk_score(
        loading_pct=loading_pct,
        oil_temp=inputs["oil_temp"],
        winding_temp=inputs["winding_temp"],
        imbalance_pct=imbalance_pct,
        voltage_dev_pct=abs(voltage_dev_pct),
        power_factor=inputs["power_factor"],
    )

    risk_level = classify_risk_level(risk_score)

    issues = evaluate_transmission_issues(
        loading_pct=loading_pct,
        oil_temp=inputs["oil_temp"],
        winding_temp=inputs["winding_temp"],
        imbalance_pct=imbalance_pct,
        voltage_dev_pct=abs(voltage_dev_pct),
        power_factor=inputs["power_factor"],
    )

    return {
        "substation_name": inputs["substation_name"],
        "transformer_mva": inputs["transformer_mva"],
        "load_mw": inputs["load_mw"],
        "primary_kv": inputs["primary_kv"],
        "secondary_kv": inputs["secondary_kv"],
        "current_r": inputs["current_r"],
        "current_y": inputs["current_y"],
        "current_b": inputs["current_b"],
        "power_factor": inputs["power_factor"],
        "oil_temp": inputs["oil_temp"],
        "winding_temp": inputs["winding_temp"],
        "loading_pct": round(loading_pct, 2),
        "avg_current": round(avg_current, 2),
        "imbalance_pct": round(imbalance_pct, 2),
        "voltage_dev_pct": round(voltage_dev_pct, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "issues": "\n".join(issues) if issues else "No major issues detected.",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_generation_input(inputs: dict) -> dict:
    utilization_pct = calculate_utilization_pct(
        actual_generation_mw=inputs["actual_generation_mw"],
        available_capacity_mw=inputs["available_capacity_mw"],
    )

    reserve_margin_mw = calculate_reserve_margin_mw(
        available_capacity_mw=inputs["available_capacity_mw"],
        actual_generation_mw=inputs["actual_generation_mw"],
    )

    risk_score = calculate_generation_risk(
        utilization_pct=utilization_pct,
        efficiency_pct=inputs["efficiency_pct"],
        reserve_margin_mw=reserve_margin_mw,
    )

    issues = []
    if utilization_pct > 95:
        issues.append("Generation utilization is critically high.")
    elif utilization_pct > 80:
        issues.append("Generation utilization is high.")

    if inputs["efficiency_pct"] < 70:
        issues.append("Plant efficiency is critically low.")
    elif inputs["efficiency_pct"] < 85:
        issues.append("Plant efficiency is below preferred target.")

    if reserve_margin_mw < 0:
        issues.append("Generation deficit detected.")
    elif reserve_margin_mw < 20:
        issues.append("Reserve margin is low.")

    return {
        "plant_name": inputs["plant_name"],
        "plant_type": inputs["plant_type"],
        "installed_capacity_mw": inputs["installed_capacity_mw"],
        "available_capacity_mw": inputs["available_capacity_mw"],
        "actual_generation_mw": inputs["actual_generation_mw"],
        "efficiency_pct": inputs["efficiency_pct"],
        "reserve_margin_mw": round(reserve_margin_mw, 2),
        "utilization_pct": round(utilization_pct, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": classify_risk_level(risk_score),
        "issues": "\n".join(issues) if issues else "No major issues detected.",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_distribution_input(inputs: dict) -> dict:
    total_loss_pct = calculate_total_loss_pct(
        technical_loss_pct=inputs["technical_loss_pct"],
        non_technical_loss_pct=inputs["non_technical_loss_pct"],
    )

    dt_loading_pct = calculate_dt_loading_pct(
        dt_load_mw=inputs["dt_load_mw"],
        dt_rating_mva=inputs["dt_rating_mva"],
    )

    risk_score = calculate_distribution_risk(
        total_loss_pct=total_loss_pct,
        consumer_voltage_v=inputs["consumer_voltage_v"],
        dt_loading_pct=dt_loading_pct,
    )

    issues = []
    if total_loss_pct > 20:
        issues.append("Distribution loss is critically high.")
    elif total_loss_pct > 12:
        issues.append("Distribution loss is above normal target.")

    if inputs["consumer_voltage_v"] < 200:
        issues.append("Consumer voltage is critically low.")
    elif inputs["consumer_voltage_v"] < 215:
        issues.append("Consumer voltage is below preferred level.")

    if dt_loading_pct > 100:
        issues.append("Distribution transformer overload detected.")
    elif dt_loading_pct > 80:
        issues.append("Distribution transformer loading is high.")

    return {
        "zone_name": inputs["zone_name"],
        "feeder_name": inputs["feeder_name"],
        "feeder_load_mw": inputs["feeder_load_mw"],
        "dt_rating_mva": inputs["dt_rating_mva"],
        "dt_load_mw": inputs["dt_load_mw"],
        "consumer_voltage_v": inputs["consumer_voltage_v"],
        "technical_loss_pct": inputs["technical_loss_pct"],
        "non_technical_loss_pct": inputs["non_technical_loss_pct"],
        "total_loss_pct": round(total_loss_pct, 2),
        "dt_loading_pct": round(dt_loading_pct, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": classify_risk_level(risk_score),
        "issues": "\n".join(issues) if issues else "No major issues detected.",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_sales_input(inputs: dict) -> dict:
    revenue_mmk = calculate_revenue_mmk(
        units_sold_mwh=inputs["units_sold_mwh"],
        tariff_mmk_per_kwh=inputs["tariff_mmk_per_kwh"],
    )

    risk_score = 0.0
    issues = []

    category_total = inputs["industrial_pct"] + inputs["residential_pct"] + inputs["commercial_pct"]
    if abs(category_total - 100.0) > 0.01:
        issues.append("Customer category percentages do not total 100%.")
        risk_score += 40

    if inputs["tariff_mmk_per_kwh"] <= 0:
        issues.append("Tariff must be greater than zero.")
        risk_score += 30

    if inputs["units_sold_mwh"] <= 0:
        issues.append("Units sold must be greater than zero.")
        risk_score += 30

    return {
        "zone_name": inputs["zone_name"],
        "units_sold_mwh": inputs["units_sold_mwh"],
        "tariff_mmk_per_kwh": inputs["tariff_mmk_per_kwh"],
        "revenue_mmk": round(revenue_mmk, 2),
        "industrial_pct": inputs["industrial_pct"],
        "residential_pct": inputs["residential_pct"],
        "commercial_pct": inputs["commercial_pct"],
        "risk_score": round(min(risk_score, 100.0), 2),
        "risk_level": classify_risk_level(risk_score),
        "issues": "\n".join(issues) if issues else "Sales input is consistent.",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_roi_input(inputs: dict) -> dict:
    annual_profit_mmk = calculate_annual_profit(
        annual_revenue_mmk=inputs["annual_revenue_mmk"],
        opex_monthly_mmk=inputs["opex_monthly_mmk"],
    )

    roi_pct = calculate_roi_pct(
        capex_mmk=inputs["capex_mmk"],
        annual_profit_mmk=annual_profit_mmk,
    )

    payback_years = calculate_payback_years(
        capex_mmk=inputs["capex_mmk"],
        annual_profit_mmk=annual_profit_mmk,
    )

    issues = []
    risk_score = 0.0

    if annual_profit_mmk <= 0:
        issues.append("Annual profit is zero or negative.")
        risk_score += 50

    if roi_pct < 5:
        issues.append("ROI is very low.")
        risk_score += 25
    elif roi_pct < 12:
        issues.append("ROI is moderate but can be improved.")
        risk_score += 10

    if payback_years > 10:
        issues.append("Payback period is long.")
        risk_score += 25
    elif payback_years > 5:
        issues.append("Payback period is moderate.")
        risk_score += 10

    return {
        "project_name": inputs["project_name"],
        "capex_mmk": inputs["capex_mmk"],
        "opex_monthly_mmk": inputs["opex_monthly_mmk"],
        "annual_revenue_mmk": inputs["annual_revenue_mmk"],
        "annual_profit_mmk": round(annual_profit_mmk, 2),
        "roi_pct": round(roi_pct, 2),
        "payback_years": round(payback_years, 2),
        "risk_score": round(min(risk_score, 100.0), 2),
        "risk_level": classify_risk_level(risk_score),
        "issues": "\n".join(issues) if issues else "ROI profile is healthy.",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_export_input(inputs: dict) -> dict:
    surplus_mw = calculate_surplus_mw(
        total_generation_mw=inputs["total_generation_mw"],
        total_demand_mw=inputs["total_demand_mw"],
    )

    export_energy_mwh = calculate_export_energy_mwh(
        surplus_mw=surplus_mw,
        export_hours=inputs["export_hours"],
    )

    export_revenue_mmk = calculate_export_revenue_mmk(
        export_energy_mwh=export_energy_mwh,
        export_tariff_mmk_per_kwh=inputs["export_tariff_mmk_per_kwh"],
    )

    issues = []
    risk_score = 0.0

    if surplus_mw < 0:
        issues.append("Generation deficit detected. No export possible.")
        risk_score += 60
    elif surplus_mw == 0:
        issues.append("No exportable surplus available.")
        risk_score += 25
    else:
        issues.append("Surplus generation available for potential export.")

    return {
        "zone_name": inputs["zone_name"],
        "total_generation_mw": inputs["total_generation_mw"],
        "total_demand_mw": inputs["total_demand_mw"],
        "surplus_mw": round(surplus_mw, 2),
        "export_hours": inputs["export_hours"],
        "export_tariff_mmk_per_kwh": inputs["export_tariff_mmk_per_kwh"],
        "export_energy_mwh": round(export_energy_mwh, 2),
        "export_revenue_mmk": round(export_revenue_mmk, 2),
        "risk_score": round(min(risk_score, 100.0), 2),
        "risk_level": classify_risk_level(risk_score),
        "issues": "\n".join(issues),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
