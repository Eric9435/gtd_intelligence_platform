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
