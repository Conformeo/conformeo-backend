def compute_score(audit) -> dict:
    total = len(audit.exigences)
    if total == 0:
        return {"score": 0, "conforme": 0, "non_conforme": 0, "critical_ko": []}
    conforme = 0
    non_conforme = 0
    critical_ko = []
    for item in audit.exigences:
        if item.answer.lower() == "oui":
            conforme += 1
        else:
            non_conforme += 1
            if item.critical:
                critical_ko.append(item.exigence.label)
    score = round(100 * conforme / total)
    return {
        "score": score,
        "conforme": conforme,
        "non_conforme": non_conforme,
        "critical_ko": critical_ko,
        "total": total,
    }
