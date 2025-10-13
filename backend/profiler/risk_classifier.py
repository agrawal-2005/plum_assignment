def classify_risk(factors: list) -> dict:
    factor_scores = {
        'smoking': 30, 'high sugar diet': 25, 'poor diet': 20,
        'low exercise': 20, 'sedentary lifestyle': 20, 'obesity': 25,
        'high blood pressure': 25, 'high cholesterol': 20,
        'diabetes': 30, 'alcohol': 15, 'stress': 15, 'sleep deprivation': 15
    }
    
    score = 0
    rationale = []

    if not factors:
        return {"risk_level": "Low", "score": 0, "rationale": []}

    for item in factors:
        factor_name = item.get("factor", "").lower().strip()
        confidence = item.get("confidence", 0.0)
        for key, value in factor_scores.items():
            if key in factor_name:
                score += value * confidence
                rationale.append(item.get("factor"))
                break
    score = min(int(round(score)), 100)

    if score > 65:
        level = "High"
    elif score > 35:
        level = "Medium"
    else:
        level = "Low"
        
    return {"risk_level": level, "score": score, "rationale": list(set(rationale))}
