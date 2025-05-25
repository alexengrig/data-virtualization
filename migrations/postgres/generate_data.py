from faker import Faker
import csv
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).parent / 'data'
BASE_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

# --- groups.csv ---
with open(BASE_DIR / 'groups.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, 11):
        writer.writerow([
            i,
            f'Group {i}',
            f'{fake.word().capitalize()} Faculty',
            fake.random_int(min=1, max=4)
        ])

# --- students.csv ---
with open(BASE_DIR / 'students.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, 10001):
        writer.writerow([
            i,
            fake.name(),
            fake.random_element(['male', 'female']),
            fake.date_of_birth(minimum_age=18, maximum_age=25),
            (i % 10) + 1
        ])

# --- courses.csv ---
with open(BASE_DIR / 'courses.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(1, 51):
        writer.writerow([
            i,
            f'Course {i}',
            f'{fake.word().capitalize()} Department'
        ])

# --- enrollments.csv ---
enrollment_id = 1
enrollments = []
semesters = ['2023-Fall', '2024-Spring', '2024-Fall']

with open(BASE_DIR / 'enrollments.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for student_id in range(1, 10001):
        for semester in semesters:
            course_ids = fake.random_elements(elements=range(1, 51), length=5, unique=True)
            for course_id in course_ids:
                writer.writerow([enrollment_id, student_id, course_id, semester])
                enrollments.append(enrollment_id)
                enrollment_id += 1

# --- grades.csv ---
with open(BASE_DIR / 'grades.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for eid in enrollments:
        writer.writerow([
            eid,
            fake.random_element(['A', 'B', 'C', 'D', 'F']),
            fake.date_between(start_date='-1y', end_date='today')
        ])

# --- attendance.csv ---
with open(BASE_DIR / 'attendance.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for eid in enrollments:
        for _ in range(10):
            writer.writerow([
                eid,
                fake.date_between(start_date='-90d', end_date='today'),
                fake.random_element(['present', 'absent', 'late'])
            ])

# --- submissions.csv ---
with open(BASE_DIR / 'submissions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for eid in enrollments:
        for i in range(1, 6):
            submitted = fake.date_time_between(start_date='-90d', end_date='now')
            due = submitted + timedelta(days=fake.random_int(min=-5, max=5))
            writer.writerow([
                eid,
                f'Task {i}',
                submitted,
                due,
                fake.random_int(min=50, max=100)
            ])
