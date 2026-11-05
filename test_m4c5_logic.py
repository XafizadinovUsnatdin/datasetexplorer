import json
import math

REQUIRED_CONTEXT_FIELDS = [
    "dataset_id",
    "split_id",
    "target",
    "positive_class",
    "features",
    "threshold",
    "seed",
    "evaluation_split"
]

MODEL_SETTINGS_FIELDS = ["model", "penalty", "C"]

def validate_metric(val):
    if val is None:
        return False, "Missing metric"
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        return False, "Metric must be a numeric value"
    if math.isnan(val) or math.isinf(val):
        return False, "Metric must be a finite number"
    if val < 0.0 or val > 1.0:
        return False, f"Metric value {val} out of range [0, 1]"
    return True, None

def parse_and_validate_run(json_str):
    try:
        data = json.loads(json_str)
    except Exception as e:
        return None, f"Malformed JSON: {e}"
    
    if not isinstance(data, dict):
        return None, "JSON root must be an object/dict"
    
    # Check format version if present
    fv = data.get("format_version")
    if fv is not None and fv != 1:
        return None, f"Unsupported format_version: {fv}"
    
    # Check metrics
    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        return None, "Missing or invalid 'metrics' dictionary"
    
    for m in ["f1", "precision", "recall"]:
        if m not in metrics:
            return None, f"Missing required metric: {m}"
        ok, err = validate_metric(metrics[m])
        if not ok:
            return None, f"Invalid metric '{m}': {err}"
            
    if "train_f1" in metrics:
        ok, err = validate_metric(metrics["train_f1"])
        if not ok:
            return None, f"Invalid metric 'train_f1': {err}"

    return data, None

def compare_experiments(data_a, data_b):
    # Check context fields in both
    missing_a = [f for f in REQUIRED_CONTEXT_FIELDS if f not in data_a or data_a[f] is None]
    missing_b = [f for f in REQUIRED_CONTEXT_FIELDS if f not in data_b or data_b[f] is None]
    
    if missing_a or missing_b:
        missing_info = []
        if missing_a:
            missing_info.append(f"A missing: {', '.join(missing_a)}")
        if missing_b:
            missing_info.append(f"B missing: {', '.join(missing_b)}")
        return {
            "status": "Insufficient context",
            "reason": "; ".join(missing_info),
            "can_compare_validation": False,
            "metrics": get_metric_deltas(data_a, data_b),
            "settings": get_settings_diff(data_a, data_b),
            "gap": None
        }

    # All context fields are present -> check for match
    diffs = []
    if data_a["dataset_id"] != data_b["dataset_id"]:
        diffs.append(f"dataset_id ('{data_a['dataset_id']}' vs '{data_b['dataset_id']}')")
    if data_a["split_id"] != data_b["split_id"]:
        diffs.append(f"split_id ('{data_a['split_id']}' vs '{data_b['split_id']}')")
    if data_a["target"] != data_b["target"]:
        diffs.append(f"target ('{data_a['target']}' vs '{data_b['target']}')")
    if data_a["positive_class"] != data_b["positive_class"]:
        diffs.append(f"positive_class ('{data_a['positive_class']}' vs '{data_b['positive_class']}')")
    if set(data_a["features"]) != set(data_b["features"]):
        diffs.append("features set mismatch")
    if data_a["threshold"] != data_b["threshold"]:
        diffs.append(f"threshold ({data_a['threshold']} vs {data_b['threshold']})")
    if data_a["seed"] != data_b["seed"]:
        diffs.append(f"seed ({data_a['seed']} vs {data_b['seed']})")
    if data_a["evaluation_split"] != data_b["evaluation_split"]:
        diffs.append(f"evaluation_split ('{data_a['evaluation_split']}' vs '{data_b['evaluation_split']}')")
    elif data_a["evaluation_split"] != "validation":
        diffs.append(f"evaluation_split is not 'validation' (both are '{data_a['evaluation_split']}')")

    status = "Same recorded conditions" if not diffs else "Conditions differ"
    reason = "All recorded context labels match" if not diffs else f"Conditions differ: {'; '.join(diffs)}"
    
    can_compare_val = (status == "Same recorded conditions")
    
    # Validation gap: available only if evaluation_split is 'validation' in both
    gap_info = None
    if data_a.get("evaluation_split") == "validation" and data_b.get("evaluation_split") == "validation":
        m_a = data_a.get("metrics", {})
        m_b = data_b.get("metrics", {})
        if "train_f1" in m_a and "f1" in m_a and "train_f1" in m_b and "f1" in m_b:
            gap_a = m_a["train_f1"] - m_a["f1"]
            gap_b = m_b["train_f1"] - m_b["f1"]
            gap_info = {
                "gap_a": round(gap_a, 2),
                "gap_b": round(gap_b, 2),
                "gap_delta": round(gap_b - gap_a, 2)
            }

    return {
        "status": status,
        "reason": reason,
        "can_compare_validation": can_compare_val,
        "metrics": get_metric_deltas(data_a, data_b),
        "settings": get_settings_diff(data_a, data_b),
        "gap": gap_info
    }

def get_metric_deltas(data_a, data_b):
    m_a = data_a.get("metrics", {})
    m_b = data_b.get("metrics", {})
    res = {}
    for m in ["f1", "precision", "recall"]:
        v_a = m_a.get(m, 0.0)
        v_b = m_b.get(m, 0.0)
        res[m] = {
            "a": v_a,
            "b": v_b,
            "delta": round(v_b - v_a, 2)
        }
    return res

def get_settings_diff(data_a, data_b):
    res = {}
    for s in MODEL_SETTINGS_FIELDS:
        v_a = data_a.get(s)
        v_b = data_b.get(s)
        diff = None
        if isinstance(v_a, (int, float)) and isinstance(v_b, (int, float)):
            diff = round(v_b - v_a, 2)
        res[s] = {"a": v_a, "b": v_b, "delta": diff}
    return res

if __name__ == "__main__":
    def load(fn):
        with open(fn, "r", encoding="utf-8") as f:
            d, err = parse_and_validate_run(f.read())
            assert err is None, err
            return d

    print("--- Test 1: M4C5_RUN_A vs M4C5_RUN_B ---")
    dA = load("M4C5_RUN_A.json")
    dB = load("M4C5_RUN_B.json")
    c1 = compare_experiments(dA, dB)
    print("Status:", c1["status"])
    print("Reason:", c1["reason"])
    print("Metrics:", c1["metrics"])
    print("Settings:", c1["settings"])
    print("Gap:", c1["gap"])
    assert c1["status"] == "Same recorded conditions"
    assert c1["metrics"]["f1"]["delta"] == 0.03
    assert c1["metrics"]["precision"]["delta"] == 0.03
    assert c1["metrics"]["recall"]["delta"] == 0.02
    assert c1["settings"]["C"]["delta"] == -0.90
    assert c1["gap"]["gap_a"] == 0.15 and c1["gap"]["gap_b"] == 0.07

    print("\n--- Test 2: Same File A vs A ---")
    c2 = compare_experiments(dA, dA)
    assert c2["status"] == "Same recorded conditions"
    assert c2["metrics"]["f1"]["delta"] == 0.0
    assert c2["settings"]["C"]["delta"] == 0.0

    print("\n--- Test 3: Swapped B vs A ---")
    c3 = compare_experiments(dB, dA)
    assert c3["status"] == "Same recorded conditions"
    assert c3["metrics"]["f1"]["delta"] == -0.03
    assert c3["metrics"]["precision"]["delta"] == -0.03
    assert c3["metrics"]["recall"]["delta"] == -0.02
    assert c3["settings"]["C"]["delta"] == 0.90

    print("\n--- Test 4: Missing Context A vs MISSING ---")
    dM = load("M4C5_MISSING_CONTEXT.json")
    c4 = compare_experiments(dA, dM)
    print("Status:", c4["status"])
    print("Reason:", c4["reason"])
    assert c4["status"] == "Insufficient context"
    assert "evaluation_split" in c4["reason"]
    assert c4["gap"] is None

    print("\n--- Test 5: Changed Split A vs CHANGED_SPLIT ---")
    dS = load("M4C5_CHANGED_SPLIT.json")
    c5 = compare_experiments(dA, dS)
    print("Status:", c5["status"])
    print("Reason:", c5["reason"])
    assert c5["status"] == "Conditions differ"
    assert "split_id" in c5["reason"]

    print("\n--- Test 6: Challenge A vs CHALLENGE (Train evaluation_split) ---")
    dC = load("M4C5_CHALLENGE.json")
    c6 = compare_experiments(dA, dC)
    print("Status:", c6["status"])
    print("Reason:", c6["reason"])
    assert c6["status"] == "Conditions differ"
    assert "evaluation_split" in c6["reason"]
    assert c6["gap"] is None

    print("\nALL 6 TEST CHECKS PASSED PERFECTLY!")

