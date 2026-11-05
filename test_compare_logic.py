import pandas as pd
import numpy as np

def is_missing(val):
    if val is None or pd.isna(val):
        return True
    if isinstance(val, str):
        return len(val.strip()) == 0
    return False

def count_missing_cells(df):
    count = 0
    for col in df.columns:
        count += sum(1 for v in df[col] if is_missing(v))
    return count

def read_csv_for_compare(file_path):
    return pd.read_csv(file_path, dtype=str, keep_default_na=False, encoding="utf-8")

def compare_datasets(before_path, after_path, id_col=None):
    df_b = read_csv_for_compare(before_path)
    df_a = read_csv_for_compare(after_path)
    
    # 1. Summary counts
    b_rows, a_rows = len(df_b), len(df_a)
    d_rows = a_rows - b_rows
    
    b_cols, a_cols = len(df_b.columns), len(df_a.columns)
    d_cols = a_cols - b_cols
    
    b_miss = count_missing_cells(df_b)
    a_miss = count_missing_cells(df_a)
    d_miss = a_miss - b_miss
    
    # 2. Columns
    added_cols = [c for c in df_a.columns if c not in df_b.columns]
    removed_cols = [c for c in df_b.columns if c not in df_a.columns]
    common_cols = [c for c in df_b.columns if c in df_a.columns]
    
    # 3. Missing in common columns
    common_missing = {}
    for c in common_cols:
        cm_b = sum(1 for v in df_b[c] if is_missing(v))
        cm_a = sum(1 for v in df_a[c] if is_missing(v))
        common_missing[c] = {"before": cm_b, "after": cm_a, "delta": cm_a - cm_b}
        
    # 4. ID validation
    id_status = "NO_ID"
    added_ids = []
    removed_ids = []
    common_ids = []
    
    if id_col and id_col in common_cols:
        s_b = df_b[id_col].astype(str)
        s_a = df_a[id_col].astype(str)
        
        b_blanks = sum(1 for v in s_b if is_missing(v))
        a_blanks = sum(1 for v in s_a if is_missing(v))
        
        b_dup = len(s_b) != len(s_b.unique())
        a_dup = len(s_a) != len(s_a.unique())
        
        if b_blanks > 0 or a_blanks > 0:
            id_status = f"BLANK_ID (BEFORE: {b_blanks}, AFTER: {a_blanks})"
        elif b_dup or a_dup:
            id_status = f"DUPLICATE_ID (BEFORE dup: {b_dup}, AFTER dup: {a_dup})"
        else:
            id_status = "VALID"
            set_b = set(s_b)
            set_a = set(s_a)
            added_ids = [i for i in s_a if i not in set_b]
            removed_ids = [i for i in s_b if i not in set_a]
            common_ids = [i for i in s_b if i in set_a]
            
    return {
        "rows": (b_rows, a_rows, d_rows),
        "cols": (b_cols, a_cols, d_cols),
        "missing": (b_miss, a_miss, d_miss),
        "added_cols": added_cols,
        "removed_cols": removed_cols,
        "common_missing": common_missing,
        "id_status": id_status,
        "added_ids": added_ids,
        "removed_ids": removed_ids,
        "common_ids": common_ids
    }

if __name__ == "__main__":
    print("--- Test 1: Main pair BEFORE -> AFTER with row_id ---")
    res1 = compare_datasets("M3C4_BEFORE.csv", "M3C4_AFTER.csv", "row_id")
    print("Rows:", res1["rows"])
    print("Cols:", res1["cols"])
    print("Missing:", res1["missing"])
    print("Added cols:", res1["added_cols"])
    print("Removed cols:", res1["removed_cols"])
    print("Common missing:", res1["common_missing"])
    print("ID status:", res1["id_status"])
    print("Added IDs:", res1["added_ids"])
    print("Removed IDs:", res1["removed_ids"])
    print("Common IDs:", res1["common_ids"])

    print("\n--- Test 2: Same file BEFORE -> BEFORE with row_id ---")
    res2 = compare_datasets("M3C4_BEFORE.csv", "M3C4_BEFORE.csv", "row_id")
    print("Rows:", res2["rows"])
    print("Missing:", res2["missing"])
    print("Added IDs:", res2["added_ids"], "Removed IDs:", res2["removed_ids"])

    print("\n--- Test 3: Swapped pair AFTER -> BEFORE with row_id ---")
    res3 = compare_datasets("M3C4_AFTER.csv", "M3C4_BEFORE.csv", "row_id")
    print("Rows:", res3["rows"])
    print("Missing:", res3["missing"])
    print("Added IDs:", res3["added_ids"])
    print("Removed IDs:", res3["removed_ids"])

    print("\n--- Test 4: Reordered rows BEFORE -> REORDERED ---")
    res4 = compare_datasets("M3C4_BEFORE.csv", "M3C4_REORDERED_BEFORE.csv", "row_id")
    print("Added IDs:", res4["added_ids"], "Removed IDs:", res4["removed_ids"])

    print("\n--- Test 5: Duplicate ID BEFORE -> DUPLICATE ---")
    res5 = compare_datasets("M3C4_BEFORE.csv", "M3C4_DUPLICATE_ID.csv", "row_id")
    print("ID status:", res5["id_status"])

    print("\n--- Test 6: Text IDs 001 and 1 ---")
    res6 = compare_datasets("M3C4_TEXT_IDS.csv", "M3C4_TEXT_IDS.csv", "row_id")
    print("Rows:", res6["rows"], "Missing:", res6["missing"], "ID status:", res6["id_status"])

