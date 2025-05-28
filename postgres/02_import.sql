COPY groups(id, name, faculty, year)
    FROM '/docker-entrypoint-initdb.d/data/groups.csv' DELIMITER ',' CSV;

COPY students(id, name, gender, birth_date, group_id)
    FROM '/docker-entrypoint-initdb.d/data/students.csv' DELIMITER ',' CSV;

COPY courses(id, name, department)
    FROM '/docker-entrypoint-initdb.d/data/courses.csv' DELIMITER ',' CSV;

COPY enrollments(id, student_id, course_id, semester)
    FROM '/docker-entrypoint-initdb.d/data/enrollments.csv' DELIMITER ',' CSV;

COPY grades(enrollment_id, grade, exam_date)
    FROM '/docker-entrypoint-initdb.d/data/grades.csv' DELIMITER ',' CSV;

COPY attendance(enrollment_id, date, status)
    FROM '/docker-entrypoint-initdb.d/data/attendance.csv' DELIMITER ',' CSV;

COPY submissions(enrollment_id, task, submitted_at, due_date, score)
    FROM '/docker-entrypoint-initdb.d/data/submissions.csv' DELIMITER ',' CSV;
