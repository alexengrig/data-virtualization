import csv
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

BASE_DIR = Path(__file__).parent / 'data'
BASE_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

sensor_types = ['temperature', 'humidity', 'co2']
auditoriums = [f'B1-{i:03}' for i in range(1, 21)] + \
              [f'A2-{i:03}' for i in range(1, 21)] + \
              [f'C3-{i:03}' for i in range(1, 21)]  # 60 аудиторий

start_time = datetime.now() - timedelta(days=30)
interval = timedelta(minutes=30)
rows_per_auditorium = int((30 * 24 * 60) / 30)  # 30 дней × 48 замеров в день

with open(BASE_DIR / 'sensor_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for auditorium in auditoriums:
        current_time = start_time
        for _ in range(rows_per_auditorium):
            writer.writerow([current_time.isoformat(), auditorium, 'temperature',
                             round(fake.pyfloat(min_value=18, max_value=30), 2)])
            writer.writerow(
                [current_time.isoformat(), auditorium, 'humidity', round(fake.pyfloat(min_value=30, max_value=90), 2)])
            writer.writerow(
                [current_time.isoformat(), auditorium, 'co2', round(fake.pyfloat(min_value=400, max_value=1600), 2)])
            current_time += interval
