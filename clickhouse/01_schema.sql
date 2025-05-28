CREATE TABLE IF NOT EXISTS platform_events
(
    event_date   Date,
    event_time   DateTime,
    user_id      UInt32,
    group_id     UInt16,
    course_id    UInt16,
    event_type LowCardinality(String),
    duration_sec UInt16,
    device_type LowCardinality(String)
) ENGINE = MergeTree()
      ORDER BY (event_date, user_id);

CREATE TABLE IF NOT EXISTS teaching_summary
(
    teacher_id        UInt32,
    full_name         String,
    department LowCardinality(String),
    semester          String,
    courses_taught    UInt8,
    lectures_total    UInt16,
    lab_hours         UInt16,
    consultations     UInt16,
    students_covered  UInt32,
    total_sessions    UInt32,
    rating_avg        Float32,
    bonus_eligible    UInt8,
    total_payment_rub Float64
) ENGINE = MergeTree()
      ORDER BY (semester, department);
