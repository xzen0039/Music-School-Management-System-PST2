Author: Xianghao Zeng
Stage: Music-School-Management-System-PST2
Music School Management System with persistence, CRUD, student check-in, badge printing and CLI.

# Overview

The Music School Management System (MSMS) is a Python-based project that manages students, teachers, attendance, and administrative functions for a music school.
It is developed in four stages as part of the PST2 coursework, each stage building upon the previous to add more features.
By Stage 4, the system includes a fully functional command-line interface.

## Stage 1 – Basic Architecture & Persistence
JSON storage (msms.json)
Auto-creates file if missing
Centralized app_data structure
load_data() / save_data() functions
Self-test mode for persistence

## Stage 2 – Core CRUD
Teacher
  Add (add_teacher)
  Update (update_teacher)
  Remove (remove_teacher)
Student
  Add (add_student)
  Update (update_student)
  Remove (remove_student)
Automatic data saving after each operation
test_crud_operations() to verify

## Stage 3 – New Feature Extension
Student Check-In
  check_in(student_id, course_id)
  Records timestamped attendance in app_data["attendance"]
Student Card Generation
  print_student_card(student_id, filename)
  Outputs a .txt file with student details
Integrated tests in test_new_features()

## Stage 4 – User Interface
Command-Line Interface (CLI)
  Interactive menu with options for all CRUD and Stage 3 features
  Input validation and error handling
  Keyboard interrupt protection
Statistics Display
  Shows total teachers, students, attendance count, and average grade
main_loop() function to start the menu system

# Example – Stage 4 CLI
=== Music School Management System ===
1. Add Teacher
2. Update Teacher
3. Remove Teacher
4. Add Student
5. Update Student
6. Remove Student
7. Student Check-in
8. Print Student Card
9. Show Statistics
10. Exit
Select option (1-10): 4
Name: Alice
Grade: 92
Student Alice added with ID 1

# Future Improvements
  Graphical interface (Tkinter / PyQt)
  Database backend (SQLite / PostgreSQL)
  Search and filtering
  Export reports (CSV / PDF)
