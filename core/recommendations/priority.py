def classify_priority(risk_score: float) -> str:
    if risk_score >= 80:
        return "URGENT"
    if risk_score >= 60:
        return "HIGH PRIORITY"
    if risk_score >= 30:
        return "MONITOR"
    return "NORMAL"


def build_priority_message(risk_score: float) -> str:
    priority = classify_priority(risk_score)

    if priority == "URGENT":
        return "Immediate corrective action recommended."
    if priority == "HIGH PRIORITY":
        return "Short-term engineering action recommended."
    if priority == "MONITOR":
        return "Continue tracking and review in next assessment cycle."
    return "No immediate intervention required."
