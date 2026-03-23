def validate_positive(name: str, value: float) -> list[str]:
    issues = []
    if value < 0:
        issues.append(f"{name} cannot be negative.")
    return issues


def validate_percentage(name: str, value: float, max_value: float = 100.0) -> list[str]:
    issues = []
    if value < 0 or value > max_value:
        issues.append(f"{name} must be between 0 and {max_value}.")
    return issues


def validate_power_factor(value: float) -> list[str]:
    issues = []
    if value <= 0 or value > 1:
        issues.append("Power factor must be greater than 0 and less than or equal to 1.")
    return issues


def validate_voltage(name: str, value: float) -> list[str]:
    issues = []
    if value <= 0:
        issues.append(f"{name} must be greater than zero.")
    return issues


def validate_category_total(values: dict) -> list[str]:
    total = sum(values.values())
    issues = []
    if abs(total - 100.0) > 0.01:
        issues.append(f"Category percentages must total 100. Current total = {total:.2f}.")
    return issues


def build_data_quality_score(issue_count: int) -> float:
    if issue_count <= 0:
        return 100.0
    score = 100.0 - (issue_count * 15.0)
    return max(score, 0.0)
