# MSMS – PST2 Final Integration
# Music School Management System with persistence, CRUD,
# student check-in, badge printing and CLI.
# Author: Xianghao Zeng

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

DATA_FILE = Path("msms.json")

# ---------- In-memory store & schema ----------
DEFAULT_DATA: Dict[str, Any] = {
    "students": [],
    "teachers": [],
    "attendance": [],
    "next_student_id": 1,
    "next_teacher_id": 1,
}

app_data: Dict[str, Any] = {**DEFAULT_DATA}


# ---------- Helpers ----------

def _ensure_schema(d: Dict[str, Any]) -> Dict[str, Any]:
    """Merge missing keys from DEFAULT_DATA and coerce simple types."""
    fixed = {**DEFAULT_DATA, **d}
    # Coerce counters to int
    for k in ("next_student_id", "next_teacher_id"):
        try:
            fixed[k] = int(fixed.get(k, 1))
        except Exception:
            fixed[k] = 1
    # Ensure lists
    for k in ("students", "teachers", "attendance"):
        if not isinstance(fixed.get(k), list):
            fixed[k] = []
    return fixed


def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    tmp.replace(path)


def _now_str() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Persistence Module ----------

def load_data(path: Path = DATA_FILE) -> bool:
    """Load data from JSON file into global app_data. Creates the file if missing."""
    global app_data
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            app_data = _ensure_schema(loaded)
            print("Data loaded successfully")
            return True
        else:
            print("Data file not found, creating new file with defaults")
            app_data = {**DEFAULT_DATA}
            save_data(path)
            return False
    except Exception as e:
        print(f"[ERROR] Load failed: {e}")
        # Fall back to defaults in memory to keep the app usable
        app_data = {**DEFAULT_DATA}
        return False


def save_data(path: Path = DATA_FILE) -> bool:
    """Save global app_data to JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(path, app_data)
        print("Data saved successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Save failed: {e}")
        return False


# ---------- ID management ----------

def _next_id(counter_key: str) -> int:
    app_data[counter_key] = int(app_data.get(counter_key, 1))
    new_id = app_data[counter_key]
    app_data[counter_key] += 1
    return new_id


# ---------- CRUD Operations ----------

_TEACHER_FIELDS = {"name", "subject"}
_STUDENT_FIELDS = {"name", "grade"}


def add_teacher(teacher_data: Dict[str, Any]) -> Tuple[bool, Optional[int]]:
    """Add a new teacher. Returns (ok, id)."""
    name = str(teacher_data.get("name", "")).strip()
    subject = str(teacher_data.get("subject", "")).strip()
    if not name or not subject:
        print("Error: 'name' and 'subject' are required to add a teacher")
        return False, None
    tid = _next_id("next_teacher_id")
    record = {"id": tid, "name": name, "subject": subject}
    app_data["teachers"].append(record)
    print(f"Teacher {name!r} added with ID {tid}")
    save_data()
    return True, tid


def update_teacher(teacher_id: int, **fields) -> bool:
    """Update teacher information (name/subject)."""
    updates = {k: v for k, v in fields.items() if k in _TEACHER_FIELDS}
    if not updates:
        print("No valid fields to update for teacher")
        return False
    for t in app_data["teachers"]:
        if t.get("id") == teacher_id:
            t.update(updates)
            print(f"Teacher ID {teacher_id} updated: {updates}")
            save_data()
            return True
    print(f"Error: Teacher ID {teacher_id} not found")
    return False


def remove_teacher(teacher_id: int) -> bool:
    """Remove teacher by ID."""
    before = len(app_data["teachers"])
    app_data["teachers"] = [t for t in app_data["teachers"] if t.get("id") != teacher_id]
    if len(app_data["teachers"]) < before:
        print(f"Teacher ID {teacher_id} removed")
        save_data()
        return True
    print(f"Error: Teacher ID {teacher_id} not found; nothing removed")
    return False


def add_student(student_data: Dict[str, Any]) -> Tuple[bool, Optional[int]]:
    """Add a new student. Returns (ok, id)."""
    name = str(student_data.get("name", "")).strip()
    if not name:
        print("Error: 'name' is required to add a student")
        return False, None
    try:
        grade_val = float(student_data.get("grade", 0.0))
    except Exception:
        print("Error: 'grade' must be a number")
        return False, None
    sid = _next_id("next_student_id")
    record = {"id": sid, "name": name, "grade": grade_val}
    app_data["students"].append(record)
    print(f"Student {name!r} added with ID {sid}")
    save_data()
    return True, sid


def update_student(student_id: int, **fields) -> bool:
    """Update student information (name/grade)."""
    updates: Dict[str, Any] = {}
    for k, v in fields.items():
        if k not in _STUDENT_FIELDS:
            continue
        if k == "grade":
            try:
                v = float(v)
            except Exception:
                print("Error: 'grade' must be a number")
                return False
        updates[k] = v
    if not updates:
        print("No valid fields to update for student")
        return False
    for s in app_data["students"]:
        if s.get("id") == student_id:
            s.update(updates)
            print(f"Student ID {student_id} updated: {updates}")
            save_data()
            return True
    print(f"Error: Student ID {student_id} not found")
    return False


def remove_student(student_id: int) -> bool:
    """Remove student by ID."""
    before = len(app_data["students"])
    app_data["students"] = [s for s in app_data["students"] if s.get("id") != student_id]
    if len(app_data["students"]) < before:
        print(f"Student ID {student_id} removed")
        save_data()
        return True
    print(f"Error: Student ID {student_id} not found; nothing removed")
    return False


# ---------- New Feature Module ----------

def check_in(student_id: int, course_id: str, timestamp: Optional[str] = None) -> bool:
    """Student check-in. `course_id` is a string like 'MUS101'."""
    student = next((s for s in app_data["students"] if s.get("id") == student_id), None)
    if not student:
        print(f"Error: Student ID {student_id} not found")
        return False
    course_id = str(course_id).strip()
    if not course_id:
        print("Error: 'course_id' must be non-empty")
        return False
    ts = timestamp or _now_str()
    record = {
        "student_id": student_id,
        "student_name": student.get("name"),
        "course_id": course_id,
        "timestamp": ts,
    }
    app_data["attendance"].append(record)
    print(f"Student {student.get('name')} (ID {student_id}) checked in for course {course_id} @ {ts}")
    save_data()
    return True


def print_student_card(student_id: int, filename: Optional[str] = None) -> bool:
    """Generate a simple text student card file."""
    student = next((s for s in app_data["students"] if s.get("id") == student_id), None)
    if not student:
        print(f"Error: Student ID {student_id} not found")
        return False
    outname = filename or f"student_{student_id}_card.txt"
    try:
        with open(outname, "w", encoding="utf-8") as f:
            f.write("=" * 40 + "\n")
            f.write("Student Card\n".center(40) + "\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"ID: {student.get('id')}\n")
            f.write(f"Name: {student.get('name')}\n")
            f.write(f"Grade: {student.get('grade')}\n\n")
            f.write("-" * 40 + "\n")
            f.write(f"Generated: {_now_str()}\n")
            f.write("=" * 40 + "\n")
        print(f"Student card saved to {outname}")
        return True
    except Exception as e:
        print(f"Failed to generate card: {e}")
        return False


# ---------- Test Code (on-demand) ----------

def test_crud_operations() -> None:
    print("\n=== CRUD Test ===")
    ok_t, tid = add_teacher({"name": "Ms. Smith", "subject": "Piano"})
    if ok_t and tid is not None:
        update_teacher(tid, subject="Vocal")

    ok_s, sid = add_student({"name": "Alice", "grade": "90.5"})
    if ok_s and sid is not None:
        update_student(sid, grade=92.0)

    print("\nCurrent Teachers:", app_data["teachers"])
    print("Current Students:", app_data["students"])

    if tid is not None:
        remove_teacher(tid)
    if sid is not None:
        remove_student(sid)

    print("After deletion – Teachers:", app_data["teachers"])
    print("After deletion – Students:", app_data["students"])


def test_new_features() -> None:
    print("\n=== New Feature Test ===")
    ok_t, tid = add_teacher({"name": "Ms. Wang", "subject": "Violin"})
    ok_s, sid = add_student({"name": "Test Student", "grade": "85.0"})

    if ok_s and sid is not None:
        print("\n1. Check-in Test:")
        check_in(sid, "MUS101")
        print("\n2. Card Generation Test:")
        print_student_card(sid, "test_card.txt")

    print("\nAttendance records:", app_data["attendance"])

    # Clean-up
    if sid is not None:
        remove_student(sid)
    if tid is not None:
        remove_teacher(tid)


# ---------- CLI entry ----------

def main() -> None:
    parser = argparse.ArgumentParser(description="MSMS – PST2 (Fixed)")
    parser.add_argument("--data", type=Path, default=DATA_FILE, help="Path to data file (default: msms.json)")
    parser.add_argument("--test", choices=["crud", "features"], help="Run a test suite")
    args = parser.parse_args()

    # Load (or initialize) data
    load_data(args.data)

    if args.test == "crud":
        test_crud_operations()
    elif args.test == "features":
        test_new_features()
    else:
        # No tests: just validate schema and save back
        print("Schema validated. Current counts -> ",
              f"students={len(app_data['students'])}",
              f"teachers={len(app_data['teachers'])}",
              f"attendance={len(app_data['attendance'])}")
        save_data(args.data)


if __name__ == "__main__":
    main()
