import os
import joblib
import numpy as np
from .schemas import ValuationRequest, ValuationResponse

MODEL_PATH = os.environ.get("AVM_MODEL_PATH", "/models/avm_catboost.joblib")

_DEF_FACTORS = [
    ("area_m2", 0.35),
    ("build_year", 0.18),
    ("rooms", 0.12),
    ("dist_to_center_km", -0.10),
    ("school_proximity", 0.08),
]

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None  # في حال عدم وجود نموذج مدرّب بعد

def predict_value(model, req: ValuationRequest) -> ValuationResponse:
    # إذا لا يوجد نموذج بعد، احسب تقديرًا بسيطًا (Baseline) لغايات الـMVP
    base = (req.area_m2 * 3500) * (1.0 + (2025 - req.build_year) * -0.01)
    base *= (1.0 + (req.school_proximity or 0) * 0.02)
    # نطاق ثقة بدائي
    ci_low, ci_high = base * 0.92, base * 1.08

    # عوامل تفسير (Placeholder) إلى أن نضيف SHAP من النموذج الفعلي
    top_factors = _DEF_FACTORS

    return ValuationResponse(
        fair_value=round(float(base), 2),
        ci_low=round(float(ci_low), 2),
        ci_high=round(float(ci_high), 2),
        currency="SAR",
        top_factors=[{"name": n, "contribution": w} for n, w in top_factors],
    )
