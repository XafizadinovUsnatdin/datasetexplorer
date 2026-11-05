# Intentionally faulty exercise. Run separately from your Explorer.
def count_added(old_ids, new_ids):
    # Buggy version: return len(new_ids) - len(old_ids)
    # Correct version: count elements in new_ids that are not in old_ids
    return len(new_ids - old_ids)

if __name__ == "__main__":
    before = {"A", "B", "C", "D", "E", "F"}
    after = {"A", "B", "C", "D", "G", "H", "I"}
    print("Added IDs count:", count_added(before, after))

