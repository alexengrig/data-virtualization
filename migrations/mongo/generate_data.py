import json
import random
from datetime import timedelta
from pathlib import Path

from faker import Faker

BASE_DIR = Path(__file__).parent / 'data'
BASE_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

# --- test_attempts.json ---
test_attempts = []
for _ in range(20000):
    student_id = random.randint(1000, 11000)
    test_id = random.choice(["sql_intro_01", "ml_basics", "data_modeling"])
    start = fake.date_time_between(start_date='-30d', end_date='now')
    duration = timedelta(minutes=random.randint(5, 40))
    end = start + duration
    answers = []
    for qid in range(1, random.randint(3, 10)):
        answers.append({
            "question_id": qid,
            "answer": random.choice(["A", "B", "C", "D"]),
            "correct": random.choice([True, False])
        })
    attempt = {
        "student_id": student_id,
        "test_id": test_id,
        "started_at": start.isoformat(),
        "finished_at": end.isoformat(),
        "score": random.randint(20, 100),
        "answers": answers,
        "device": random.choice(["desktop", "mobile", "tablet"]),
        "location": fake.country_code()
    }
    test_attempts.append(attempt)

with open(BASE_DIR / 'test_attempts.json', 'w') as f:
    for doc in test_attempts:
        f.write(json.dumps(doc) + '\n')

# --- survey_responses.json ---
surveys = []
survey_ids = ["teacher_feedback_spring24", "course_quality_2024", "platform_usability"]

for _ in range(5000):
    responses = []
    for _ in range(random.randint(3, 6)):
        qtype = random.choice(["rating", "text", "boolean"])
        if qtype == "rating":
            value = random.randint(1, 5)
        elif qtype == "text":
            value = fake.sentence()
        else:
            value = random.choice([True, False])
        responses.append({
            "question": fake.sentence(nb_words=5).rstrip('.'),
            "type": qtype,
            "value": value
        })

    surveys.append({
        "student_id": random.randint(1000, 11000),
        "survey_id": random.choice(survey_ids),
        "submitted_at": fake.date_time_between(start_date='-20d', end_date='now').isoformat(),
        "responses": responses
    })

with open(BASE_DIR / 'survey_responses.json', 'w') as f:
    for doc in surveys:
        f.write(json.dumps(doc) + '\n')
