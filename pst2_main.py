# MSMS – PST2 Final Integration
# Music School Management System with persistence, CRUD,
# student check-in, badge printing and CLI.
# Author: Xianghao Zeng

import json
import datetime
import os
from typing import Dict, Any, Optional

DATA_FILE = "msms.json"
app_data: Dict[str, Any] = {
    "students": [],
    "teachers": [],
    "attendance": [],
    "next_student_id": 1,
    "next_teacher_id": 1,
}

# ---------- Persistence ----------
def load_data(path: str = DATA_FILE) -> bool:
    """Load application data from JSON."""
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
    """Save application state to JSON."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(app_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Save failed: {e}")
        return False

# ---------- CRUD – Teachers ----------
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

# ---------- CRUD – Students ----------
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
            if "grade" in fields:
                try:
                    fields["grade"] = float(fields["grade"])
                except ValueError:
                    print("Grade must be numeric")
                    return False
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

# ---------- New Features ----------
def check_in(student_id: int, course_id: str, timestamp: Optional[str] = None) -> bool:
    """Student check-in."""
    student = next((s for s in app_data["students"] if s["id"] == student_id), None)
    if not student:
        print(f"Error: Student ID {student_id} not found")
        return False
    timestamp = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {"student_id": student_id, "student_name": student["name"],
              "course_id": course_id, "timestamp": timestamp}
    app_data["attendance"].append(record)
    print(f"Student {student['name']} (ID {student_id}) checked in for course {course_id}")
    save_data()
    return True

def print_student_card(student_id: int, filename: Optional[str] = None) -> bool:
    """Generate and save a student card."""
    student = next((s for s in app_data["students"] if s["id"] == student_id), None)
    if not student:
        print(f"Error: Student ID {student_id} not found")
        return False
    filename = filename or f"student_{student_id}_card.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 40 + "\n")
            f.write("Student Card\n".center(40) + "\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"ID: {student['id']}\n")
            f.write(f"Name: {student['name']}\n")
            f.write(f"Grade: {student.get('grade', 'N/A')}\n\n")
            f.write("-" * 40 + "\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 40 + "\n")
        print(f"Student card saved to {filename}")
        return True
    except Exception as e:
        print(f"Failed to generate card: {e}")
        return False

# ---------- CLI ----------
def display_menu() -> str:
    """Display the main menu."""
    print("\n=== Music School Management System ===")
    print("1. Add Teacher")
    print("2. Update Teacher")
    print("3. Remove Teacher")
    print("4. Add Student")
    print("5. Update Student")
    print("6. Remove Student")
    print("7. Student Check-in")
    print("8. Print Student Card")
    print("9. Show Statistics")
    print("10. Exit")
    return input("Select option (1-10): ").strip()

def get_teacher_input() -> Optional[Dict[str, str]]:
    """Collect teacher input."""
    try:
        name = input("Name: ").strip()
        subject = input("Subject: ").strip()
        return {"name": name, "subject": subject} if name and subject else None
    except Exception:
        print("Input error")
        return None

def get_student_input() -> Optional[Dict[str, Any]]:
    """Collect student input."""
    try:
        name = input("Name: ").strip()
        grade_str = input("Grade: ").strip()
        if not name:
            print("Name cannot be empty")
            return None
        grade = float(grade_str)
        if 0 <= grade <= 100:
            return {"name": name, "grade": grade}
        print("Grade must be between 0 and 100")
        return None
    except ValueError:
        print("Grade must be numeric")
        return None

def get_update_fields() -> Dict[str, str]:
    """Collect fields to update."""
    fields = {}
    print("Enter fields to update (blank to finish):")
    while True:
        key = input("Field (name/subject/grade): ").strip().lower()
        if not key:
            break
        value = input(f"New {key}: ").strip()
        fields[key] = value
    return fields

def show_statistics() -> None:
    """Display system statistics."""
    print("\n=== System Statistics ===")
    print(f"Teachers: {len(app_data.get('teachers', []))}")
    print(f"Students: {len(app_data.get('students', []))}")
    print(f"Attendance: {len(app_data.get('attendance', []))}")
    students = app_data.get("students", [])
    if students:
        grades = [s.get("grade", 0) for s in students if "grade" in s]
        if grades:
            avg = sum(grades) / len(grades)
            print(f"Average Grade: {avg:.2f}")

def main_loop() -> None:
    """Main CLI loop."""
    load_data()
    print("=== Music School Management System ===")
    print("Data loaded, system ready")
    while True:
        try:
            choice = display_menu()
            if choice == "1":
                data = get_teacher_input()
                if data:
                    add_teacher(data)
            elif choice == "2":
                try:
                    tid = int(input("Teacher ID: ").strip())
                    fields = get_update_fields()
                    if fields:
                        update_teacher(tid, **fields)
                except ValueError:
                    print("ID must be a number")
            elif choice == "3":
                try:
                    remove_teacher(int(input("Teacher ID: ").strip()))
                except ValueError:
                    print("ID must be a number")
            elif choice == "4":
                data = get_student_input()
                if data:
                    add_student(data)
            elif choice == "5":
                try:
                    sid = int(input("Student ID: ").strip())
                    fields = get_update_fields()
                    if fields:
                        update_student(sid, **fields)
                except ValueError:
                    print("ID must be a number")
            elif choice == "6":
                try:
                    remove_student(int(input("Student ID: ").strip()))
                except ValueError:
                    print("ID must be a number")
            elif choice == "7":
                try:
                    check_in(int(input("Student ID: ").strip()), input("Course ID: ").strip())
                except ValueError:
                    print("Student ID must be a number")
            elif choice == "8":
                try:
                    sid = int(input("Student ID: ").strip())
                    fname = input("Filename (optional): ").strip()
                    print_student_card(sid, fname if fname else None)
                except ValueError:
                    print("ID must be a number")
            elif choice == "9":
                show_statistics()
            elif choice == "10":
                if input("Confirm exit? (y/n): ").lower() == "y":
                    print("Goodbye!")
                    break
            else:
                print("Invalid choice")
        except KeyboardInterrupt:
            print("\nOperation interrupted. Enter 10 to exit.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_loop()
