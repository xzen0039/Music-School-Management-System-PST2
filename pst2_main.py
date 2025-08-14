# MSMS – PST2 Final Integration
# Music School Management System with persistence, CRUD,
# student check-in, badge printing and CLI.
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

# ---------- CRUD Operations ----------
def add_teacher(teacher_data: Dict[str, Any]) -> bool:
    """Add a new teacher."""
    tid = app_data["next_teacher_id"]
    app_data["next_teacher_id"] += 1
    teacher_record = {"id": tid, "name": teacher_data["name"], "subject": teacher_data["subject"]}
    app_data["teachers"].append(teacher_record)
    print(f"Teacher {teacher_data['name']} added with ID {tid}")
    save_data()
    return True

def update_teacher(teacher_id: int, **fields) -> bool:
    """Update teacher information."""
    for t in app_data["teachers"]:
        if t["id"] == teacher_id:
            t.update(fields)
            print(f"Teacher ID {teacher_id} updated")
            save_data()
            return True
    print(f"Error: Teacher ID {teacher_id} not found")
    return False

def remove_teacher(teacher_id: int) -> bool:
    """Remove teacher by ID."""
    app_data["teachers"] = [t for t in app_data["teachers"] if t["id"] != teacher_id]
    print(f"Teacher ID {teacher_id} removed")
    save_data()
    return True

def add_student(student_data: Dict[str, Any]) -> bool:
    """Add a new student."""
    sid = app_data["next_student_id"]
    app_data["next_student_id"] += 1
    student_record = {"id": sid, "name": student_data["name"], "grade": float(student_data["grade"])}
    app_data["students"].append(student_record)
    print(f"Student {student_data['name']} added with ID {sid}")
    save_data()
    return True

def update_student(student_id: int, **fields) -> bool:
    """Update student information."""
    for s in app_data["students"]:
        if s["id"] == student_id:
            s.update(fields)
            print(f"Student ID {student_id} updated")
            save_data()
            return True
    print(f"Error: Student ID {student_id} not found")
    return False

def remove_student(student_id: int) -> bool:
    """Remove student by ID."""
    app_data["students"] = [s for s in app_data["students"] if s["id"] != student_id]
    print(f"Student ID {student_id} removed")
    save_data()
    return True

# ---------- Test Code ----------
def test_crud_operations() -> None:
    """Run CRUD tests."""
    print("\n=== CRUD Test ===")

    # Add teacher
    print("\n1. Add Teacher:")
    add_teacher({"name": "Ms. Smith", "subject": "Piano"})

    # Update teacher
    print("\n2. Update Teacher:")
    update_teacher(1, subject="Vocal")

    # Add student
    print("\n3. Add Student:")
    add_student({"name": "Alice", "grade": "90.5"})

    # Update student
    print("\n4. Update Student:")
    update_student(1, grade=92.0)

    # Show current data
    print("\nCurrent Teachers:", app_data["teachers"])
    print("Current Students:", app_data["students"])

    # Delete test
    print("\n5. Delete Test:")
    remove_teacher(1)
    remove_student(1)
    print("After deletion – Teachers:", app_data["teachers"])
    print("After deletion – Students:", app_data["students"])

if __name__ == "__main__":
    load_data()
    test_crud_operations()
    print("\nCRUD test completed!")
