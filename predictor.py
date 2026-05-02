"""
predictor.py - Real-life grounded logic for everyday acne users.
"""

import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

with open(os.path.join(MODEL_DIR, "acne_rf_model.pkl"),  "rb") as f: MODEL = pickle.load(f)
with open(os.path.join(MODEL_DIR, "label_encoders.pkl"), "rb") as f: ENCODERS = pickle.load(f)
with open(os.path.join(MODEL_DIR, "feature_cols.pkl"),   "rb") as f: FEATURE_COLS = pickle.load(f)

INGREDIENTS = {
    "hormonal": [
        ("Niacinamide 5-10%",     "Regulates sebum and calms redness"),
        ("Azelaic Acid 10-20%",   "Reduces hormonal breakout severity, safe long-term"),
        ("Salicylic Acid 1-2%",   "Keeps chin and jawline pores clear"),
        ("Zinc supplement",       "Clinically shown to lower androgen-related oil"),
    ],
    "fungal": [
        ("Zinc Pyrithione wash",  "Directly targets Malassezia yeast"),
        ("Ketoconazole shampoo",  "Use as body/back wash, highly effective"),
        ("Sulfur cleanser",       "Antifungal without disrupting skin barrier"),
        ("Avoid fatty esters/oils", "Malassezia feeds on certain fatty acids"),
    ],
    "bacterial": [
        ("Benzoyl Peroxide 2.5%", "Kills C. acnes bacteria - most evidence-backed"),
        ("Salicylic Acid 2%",     "Clears pores and reduces cheek congestion"),
        ("Tea Tree Oil diluted",  "Natural antibacterial alternative"),
        ("Niacinamide 5%",        "Calms post-bacterial redness and dark marks"),
    ],
    "lifestyle": [
        ("Salicylic Acid 1-2%",   "Gentle daily exfoliation for mild breakouts"),
        ("Niacinamide 5%",        "Balances oiliness and pore appearance"),
        ("Centella Asiatica",     "Soothes mild inflammation caused by lifestyle stress"),
        ("SPF 30+ non-comedogenic","Prevents breakouts from worsening under sun"),
    ],
}

ROUTINES = {
    "hormonal": {
        "morning": ["Gentle low-pH cleanser", "Niacinamide 5% serum", "Light moisturiser", "SPF 30+"],
        "night":   ["Double cleanse (oil then foam)", "Azelaic acid or salicylic acid", "Hydrating moisturiser"],
    },
    "fungal": {
        "morning": ["Zinc pyrithione wash", "Light gel moisturiser", "SPF"],
        "night":   ["Antifungal wash immediately after sweating", "Sulfur spot treatment"],
    },
    "bacterial": {
        "morning": ["Salicylic acid cleanser", "Benzoyl peroxide spot treatment", "Oil-free moisturiser", "SPF 30+"],
        "night":   ["Benzoyl peroxide cleanser", "BHA toner or retinol", "Non-comedogenic moisturiser"],
    },
    "lifestyle": {
        "morning": ["Gentle cleanser", "Niacinamide 5%", "Lightweight moisturiser", "SPF 30+"],
        "night":   ["Gentle cleanser", "Centella Asiatica serum", "Barrier-supporting moisturiser"],
    },
}


def _build_causes(acne_type, u):
    causes = []
    if acne_type == "hormonal":
        if u["stress_level"] >= 7:
            causes.append(f"Stress level {u['stress_level']}/10 directly raises cortisol, triggering excess oil and chin/jaw breakouts")
        if u["sleep_hours"] < 6:
            causes.append(f"Only {u['sleep_hours']}h sleep disrupts androgen regulation - hormonal acne peaks with sleep deprivation")
        causes.append("Chin and jawline location is the classic hormonal acne zone in both men and women")

    elif acne_type == "fungal":
        causes.append(f"Heavy sweating ({u['sweat_level']}/10) during exercise feeds Malassezia yeast on skin surface")
        causes.append("Back acne with sweat is textbook fungal - it looks like acne but won't respond to regular acne products")
        causes.append("Showering within 30 minutes of exercise would prevent most of this")

    elif acne_type == "bacterial":
        if u["water_intake_liters"] < 1.5:
            causes.append(f"Only {u['water_intake_liters']}L water/day forces your skin to overproduce oil - pores clog and bacteria multiply")
        if u["diet_type"] == "junk":
            causes.append("Junk food spikes blood sugar and insulin, directly increasing sebum and feeding C. acnes bacteria")
        causes.append(f"Cheek and forehead location suggests contact contamination - phone screens, hands, and pillowcases are main culprits")

    else:  # lifestyle
        if u["sleep_hours"] < 6:
            causes.append(f"Sleeping {u['sleep_hours']}h causes low-grade skin inflammation that shows up as mild but persistent acne")
        if u["water_intake_liters"] < 2.0:
            causes.append(f"At {u['water_intake_liters']}L/day you are mildly dehydrated - skin loses oil regulation ability")
        causes.append("No single dominant cause - a mix of inconsistent habits creating a mild inflammatory state")

    return causes[:3]


def _build_tips(acne_type, u):
    tips = []
    if acne_type == "hormonal":
        tips.append("Your #1 lever: reduce stress. Even 10 minutes of walking daily measurably lowers cortisol")
        if u["sleep_hours"] < 7:
            tips.append(f"Push sleep from {u['sleep_hours']}h to 7+ hours - chin and jawline will visibly improve within 2 weeks")
        tips.append("Track breakouts: if they spike at certain times of month it confirms the hormonal root cause")

    elif acne_type == "fungal":
        tips.append("Shower within 30 minutes of any workout - this one change could clear most of your back acne")
        tips.append("Switch to 100% cotton or moisture-wicking gym shirts - synthetic fabric traps sweat against skin")
        tips.append("Wash gym clothes after every session, not every 2-3 uses")

    elif acne_type == "bacterial":
        if u["water_intake_liters"] < 2.0:
            tips.append(f"Increase from {u['water_intake_liters']}L to 2.5L water daily - likely your fastest visible improvement")
        tips.append("Change pillowcase every 2-3 days and clean your phone screen daily - direct bacteria transfer to cheeks")
        if u["diet_type"] == "junk":
            tips.append("Cut one junk meal per day for 2 weeks and observe change before going all-in on diet")

    else:  # lifestyle
        tips.append("Fix ONE habit first - sleep, water, or diet - not all three at once or you will give up")
        tips.append("Keep a 2-week skin diary: log sleep, diet, stress, and breakouts each day to spot your personal trigger")
        tips.append("A simple consistent 2-step routine (cleanser + SPF) beats expensive products used inconsistently")

    return tips


def _severity_score(severity, stress, sleep, water):
    score = (
        severity * 2.5
        + (stress / 10) * 1.5
        + max(0, (7 - sleep) / 7) * 1.0
        + max(0, (2.5 - water) / 2.5) * 1.0
    )
    score = min(round(score, 1), 10.0)
    risk  = "Low" if score <= 3.5 else ("Moderate" if score <= 6.5 else "High")
    return {"score": score, "risk": risk}


def _top_factor(acne_type, u):
    if acne_type == "hormonal":
        if u["stress_level"] >= 8:   return f"Very high stress ({u['stress_level']}/10)"
        if u["sleep_hours"] <= 5:    return f"Only {u['sleep_hours']}h sleep per night"
        return "Chin/jawline hormonal breakout pattern"
    if acne_type == "fungal":
        return f"Sweat buildup from exercise ({u['sweat_level']}/10 sweat)"
    if acne_type == "bacterial":
        if u["water_intake_liters"] < 1.5: return f"Critically low water intake ({u['water_intake_liters']}L/day)"
        if u["diet_type"] == "junk":       return "Junk food diet driving bacterial growth"
        return "Bacterial overgrowth in clogged pores"
    if u["sleep_hours"] < 6:     return f"Insufficient sleep ({u['sleep_hours']}h)"
    if u["diet_type"] == "junk": return "Diet causing mild persistent inflammation"
    return "Mix of inconsistent lifestyle habits"


def predict(user_input: dict) -> dict:
    row = {}
    for col in FEATURE_COLS:
        val = user_input[col]
        if col in ENCODERS:
            val = ENCODERS[col].transform([val])[0]
        row[col] = val

    X = pd.DataFrame([[row[col] for col in FEATURE_COLS]], columns=FEATURE_COLS)

    pred_enc   = MODEL.predict(X)[0]
    probs      = MODEL.predict_proba(X)[0]
    acne_type  = ENCODERS["acne_type"].inverse_transform([pred_enc])[0]
    confidence = round(float(probs.max()) * 100, 1)
    class_probs = {cls: round(float(p)*100,1) for cls, p in zip(ENCODERS["acne_type"].classes_, probs)}

    sev = _severity_score(
        user_input["severity"], user_input["stress_level"],
        user_input["sleep_hours"], user_input["water_intake_liters"]
    )

    return {
        "acne_type":      acne_type,
        "confidence":     confidence,
        "class_probs":    class_probs,
        "severity_score": sev["score"],
        "risk_level":     sev["risk"],
        "top_factor":     _top_factor(acne_type, user_input),
        "causes":         _build_causes(acne_type, user_input),
        "ingredients":    INGREDIENTS[acne_type],
        "routine":        ROUTINES[acne_type],
        "lifestyle_tips": _build_tips(acne_type, user_input),
    }
