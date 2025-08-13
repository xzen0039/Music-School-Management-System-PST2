# PST2 – Stage 1: Basic Architecture
# Data-persistence module
# Author: Xianghao Zeng

import json
import os
from typing import Dict, Any

DATA_FILE = "msms.json"
app_data: Dict[str, Any] = {
    "students": [],
    "teachers": [],
    "next_student_id": 1,
    "next_teacher_id": 1,
}

# ---------- Persistence Module ----------
def load_data(path: str = DATA_FILE) -> bool:
    """Load data from JSON file."""
    global app_data
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                app_data = json.load(f)
            print("Data loaded successfully")
            return True
        else:
            print("Data file not found, creating new file")
            save_data(path)
            return False
    except Exception as e:
        print(f"[ERROR] Load failed: {e}")
        return False

def save_data(path: str = DATA_FILE) -> bool:
    """Save data to JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(app_data, f, indent=4, ensure_ascii=False)
        print("Data saved successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Save failed: {e}")
        return False

# ---------- Test Code ----------
if __name__ == "__main__":
    print("=== Music School Management System – Architecture Test ===")
    print("1. Loading data...")
    load_data()

    print("\n2. Adding test data...")
    app_data["students"].append({"id": 1, "name": "Test Student"})
    app_data["teachers"].append({"id": 1, "name": "Test Teacher"})

    print("\n3. Saving data...")
    save_data()

    print("\n4. Verifying structure:")
    print(f"Students: {len(app_data['students'])}")
    print(f"Teachers: {len(app_data['teachers'])}")
    print(f"Next Student ID: {app_data['next_student_id']}")
    print(f"Next Teacher ID: {app_data['next_teacher_id']}")

    print("\nTest completed! Check msms.json file.")
