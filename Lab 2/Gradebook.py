# Project Title: Simplified GradeBook Analyzer CLI
# Author: Vinayak [2501730150]

import statistics

def get_student_data():
    print("\n--- Start Manual Data Entry ---")
    
    student_names = []
    student_marks = []
    
    # Simple loop to collect data
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done' or name == '':
            break
        
        while True:
            try:
                mark = int(input(f"Enter mark for {name}: "))
                if 0 <= mark <= 100:
                    student_names.append(name)
                    student_marks.append(mark)
                    break
                else:
                    print("Mark must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")
                
    return student_names, student_marks


def run_simple_analyzer():
    print("==========================================")
    print("        Simple GradeBook Analyzer        ")
    print("==========================================")
    
    names, marks = get_student_data()
    
    if not marks:
        print("No student data provided. Exiting.")
        return
    
    grades = []
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    for mark in marks:
        if mark >= 90:
            grade = 'A'
        elif mark >= 80:
            grade = 'B'
        elif mark >= 70:
            grade = 'C'
        elif mark >= 60:
            grade = 'D'
        else:
            grade = 'F'
            
        grades.append(grade)
        grade_distribution[grade] += 1

    total_students = len(marks)
    average_mark = statistics.mean(marks) 
    median_mark = statistics.median(marks) 
    max_score = max(marks)
    min_score = min(marks)
    
    
    # --- Print Statistical Summary ---
    print("\n==========================================")
    print("           Statistical Summary          ")
    print("==========================================")
    print(f"Total Students: {total_students}")
    print(f"Average Mark:   {average_mark:.2f}")
    print(f"Median Mark:    {median_mark:.2f}")
    print(f"Max Score:      {max_score}")
    print(f"Min Score:      {min_score}")
    passed_students = [name for name, mark in zip(names, marks) if mark >= 40]
    failed_students = [name for name, mark in zip(names, marks) if mark < 40]

    print("\n Pass/Fail & Distribution Summary ")
    print(f"Passed Students ({len(passed_students)}): {', '.join(passed_students) if passed_students else 'None'}")
    print(f"Failed Students ({len(failed_students)}): {', '.join(failed_students) if failed_students else 'None'}")
    
    print("\nGrade Counts:")
    for grade, count in grade_distribution.items():
        print(f"  Grade {grade}: {count}")
    
    
    # --- Task 6: Results Table ---
    print("\n==========================================")
    print("           Detailed Results Table         ")
    print("==========================================")
    print(f"{'Name':<15}{'Marks':>8}{'Grade':>8}")
    print("-" * 31)
    
    # zip names, marks, and grades together for easy printing
    for name, mark, grade in zip(names, marks, grades):
        print(f"{name:<15}{mark:>8}{grade:>8}")
    print("-" * 31)
    print("Analysis Complete. ")

if __name__ == "__main__":
    run_simple_analyzer()