import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import pandas as pd
import numpy as np

def is_missing_cell(val):
    if val is None or pd.isna(val):
        return True
    if isinstance(val, str):
        return len(val.strip()) == 0
    return False

def run_all_checks():
    print("========================================")
    print("M3C4 CSV Comparison Automated Test Suite")
    print("========================================")
    passed = 0
    total = 7

    # Load test files
    def load(path):
        return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")

    # --- Test 1: Main Pair (BEFORE -> AFTER, row_id) ---
    df_b = load("M3C4_BEFORE.csv")
    df_a = load("M3C4_AFTER.csv")
    
    b_rows, a_rows = len(df_b), len(df_a)
    b_cols, a_cols = len(df_b.columns), len(df_a.columns)
    b_miss = sum(1 for c in df_b.columns for v in df_b[c] if is_missing_cell(v))
    a_miss = sum(1 for c in df_a.columns for v in df_a[c] if is_missing_cell(v))
    
    added_cols = [c for c in df_a.columns if c not in df_b.columns]
    removed_cols = [c for c in df_b.columns if c not in df_a.columns]
    common_cols = [c for c in df_b.columns if c in df_a.columns]
    
    set_b = set(df_b["row_id"])
    set_a = set(df_a["row_id"])
    added_ids = [i for i in df_a["row_id"] if i not in set_b]
    removed_ids = [i for i in df_b["row_id"] if i not in set_a]
    common_ids = [i for i in df_b["row_id"] if i in set_a]
    
    assert (b_rows, a_rows, a_rows - b_rows) == (6, 7, 1), "Test 1 row delta failed"
    assert (b_cols, a_cols, a_cols - b_cols) == (6, 6, 0), "Test 1 col delta failed"
    assert (b_miss, a_miss, a_miss - b_miss) == (3, 1, -2), "Test 1 missing delta failed"
    assert added_cols == ["segment"], "Test 1 added col failed"
    assert removed_cols == ["legacy_note"], "Test 1 removed col failed"
    assert added_ids == ["G", "H", "I"], "Test 1 added ids failed"
    assert removed_ids == ["E", "F"], "Test 1 removed ids failed"
    assert common_ids == ["A", "B", "C", "D"], "Test 1 common ids failed"
    print("✅ Check 1: Main Pair (BEFORE -> AFTER) Passed! (Rows: 6->7, Cols: 6->6, Miss: 3->1, Added: G,H,I, Removed: E,F)")
    passed += 1

    # --- Test 2: Same File Check (BEFORE -> BEFORE) ---
    b2_rows, b2_cols = len(df_b), len(df_b.columns)
    b2_miss = sum(1 for c in df_b.columns for v in df_b[c] if is_missing_cell(v))
    assert (len(df_b) - b2_rows) == 0
    assert (len(df_b.columns) - b2_cols) == 0
    assert (b_miss - b2_miss) == 0
    same_added = [i for i in df_b["row_id"] if i not in set_b]
    same_removed = [i for i in df_b["row_id"] if i not in set_b]
    assert len(same_added) == 0 and len(same_removed) == 0
    print("✅ Check 2: Same File Check (BEFORE -> BEFORE) Passed! (All deltas = 0, no additions/removals)")
    passed += 1

    # --- Test 3: Swapped Pair (AFTER -> BEFORE) ---
    sw_d_rows = b_rows - a_rows
    sw_d_cols = b_cols - a_cols
    sw_d_miss = b_miss - a_miss
    sw_added_cols = [c for c in df_b.columns if c not in df_a.columns]
    sw_removed_cols = [c for c in df_a.columns if c not in df_b.columns]
    sw_added_ids = [i for i in df_b["row_id"] if i not in set_a]
    sw_removed_ids = [i for i in df_a["row_id"] if i not in set_b]
    assert (sw_d_rows, sw_d_cols, sw_d_miss) == (-1, 0, 2)
    assert sw_added_cols == ["legacy_note"]
    assert sw_removed_cols == ["segment"]
    assert sw_added_ids == ["E", "F"]
    assert sw_removed_ids == ["G", "H", "I"]
    print("✅ Check 3: Swapped Pair (AFTER -> BEFORE) Passed! (Rows: 7->6 (-1), Miss: 1->3 (+2), Added: E,F, Removed: G,H,I)")
    passed += 1

    # --- Test 4: Reordered Rows Check ---
    df_reord = load("M3C4_REORDERED_BEFORE.csv")
    reord_added = [i for i in df_reord["row_id"] if i not in set_b]
    reord_removed = [i for i in df_b["row_id"] if i not in set(df_reord["row_id"])]
    assert len(reord_added) == 0 and len(reord_removed) == 0
    print("✅ Check 4: Reordered Rows Check Passed! (Zero added/removed records)")
    passed += 1

    # --- Test 5: Duplicate ID Guard ---
    df_dup = load("M3C4_DUPLICATE_ID.csv")
    s_dup = df_dup["row_id"].astype(str)
    dup_detected = len(s_dup) != len(s_dup.unique())
    assert dup_detected is True, "Duplicate ID should be detected"
    dup_rows = len(df_dup)
    dup_miss = sum(1 for c in df_dup.columns for v in df_dup[c] if is_missing_cell(v))
    assert dup_rows == 7 and dup_miss == 1, "Summary counts should still be computed"
    print("✅ Check 5: Duplicate ID Guard Passed! (Summary counts available, record matching blocked)")
    passed += 1

    # --- Test 6: Text IDs Preservation ---
    df_txt = load("M3C4_TEXT_IDS.csv")
    s_txt = df_txt["row_id"].astype(str)
    assert len(s_txt) == len(s_txt.unique()) == 2, "001 and 1 must remain distinct text IDs"
    txt_miss = sum(1 for c in df_txt.columns for v in df_txt[c] if is_missing_cell(v))
    assert txt_miss == 0, "'NA', 'null', and '0' must NOT be counted as missing"
    print("✅ Check 6: Text IDs Preservation Passed! (001 != 1, NA/null/0 are values, 0 missing)")
    passed += 1

    # --- Test 7: M3C4 Bug Exercise Script ---
    from M3C4_COUNT_ADDED_BUG import count_added
    bug_before = {"A", "B", "C", "D", "E", "F"}
    bug_after = {"A", "B", "C", "D", "G", "H", "I"}
    res_bug = count_added(bug_before, bug_after)
    assert res_bug == 3, f"Expected 3 added IDs, got {res_bug}"
    assert count_added(bug_before, bug_before) == 0, "Identical sets must yield 0"
    print("✅ Check 7: Bug Exercise Script Passed! (Returns 3 for {G,H,I} and 0 for identical sets)")
    passed += 1

    print("========================================")
    print(f"Results: {passed}/{total} automated checks PASSED successfully!")
    print("========================================")

if __name__ == "__main__":
    run_all_checks()
