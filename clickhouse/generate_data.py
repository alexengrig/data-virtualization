import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

BASE_DIR = Path(__file__).parent / 'data'
BASE_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

# --- platform_events.csv ---
event_types = ['login', 'view', 'submit', 'download']
device_types = ['desktop', 'mobile', 'tablet']
start_time = datetime.now() - timedelta(days=30)

with open(BASE_DIR / 'platform_events.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for _ in range(1_000_000):
        dt = start_time + timedelta(seconds=random.randint(0, 30 * 86400))
        writer.writerow([
            dt.date().isoformat(),
            dt.strftime('%Y-%m-%d %H:%M:%S'),  # ← исправлен формат без микросекунд
            random.randint(1, 10000),
            random.randint(1, 100),
            random.randint(1, 50),
            random.choice(event_types),
            random.randint(10, 600),
            random.choice(device_types)
        ])

# --- teaching_summary.csv ---
semesters = ['2023-Fall', '2024-Spring', '2024-Fall']
departments = ['Physics', 'Mathematics', 'Computer Science', 'Economics', 'History']

with open(BASE_DIR / 'teaching_summary.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for teacher_id in range(1, 501):
        full_name = fake.name()
        department = random.choice(departments)
        for semester in semesters:
            courses = random.randint(1, 4)
            lectures = random.randint(10, 60)
            labs = random.randint(5, 30)
            consultations = random.randint(5, 20)
            students = random.randint(20, 200)
            sessions = lectures + labs + consultations
            rating = round(random.uniform(3.0, 5.0), 2)
            bonus = int(rating > 4.2)
            payment = round(lectures * 500 + labs * 400 + consultations * 300 + (bonus * 10000), 2)

            writer.writerow([
                teacher_id,
                full_name,
                department,
                semester,
                courses,
                lectures,
                labs,
                consultations,
                students,
                sessions,
                rating,
                bonus,
                payment
            ])
