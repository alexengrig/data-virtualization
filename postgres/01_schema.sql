CREATE TABLE groups
(
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    faculty TEXT NOT NULL,
    year    INT  NOT NULL
);

CREATE TABLE students
(
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    gender     TEXT,
    birth_date DATE,
    group_id   INT REFERENCES groups (id)
);

CREATE TABLE courses
(
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE enrollments
(
    id         SERIAL PRIMARY KEY,
    student_id INT REFERENCES students (id),
    course_id  INT REFERENCES courses (id),
    semester   TEXT NOT NULL
);

CREATE TABLE grades
(
    id            SERIAL PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments (id),
    grade         TEXT,
    exam_date     DATE
);

CREATE TABLE attendance
(
    id            SERIAL PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments (id),
    date          DATE NOT NULL,
    status        TEXT CHECK (status IN ('present', 'absent', 'late'))
);

CREATE TABLE submissions
(
    id            SERIAL PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments (id),
    task          TEXT      NOT NULL,
    submitted_at  TIMESTAMP NOT NULL,
    due_date      TIMESTAMP NOT NULL,
    score         NUMERIC(5, 2)
);
