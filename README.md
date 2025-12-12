# Data Virtualization

Comparison of Dremio and Trino on PostgreSQL, TimescaleDB, and MongoDB.

## Run

```shell
docker compose -f docker-compose.db.yml -f docker-compose.dremio.yml -f docker-compose.trino.yml up -d
```

## PostgreSQL

### Case 1

#### Query

```sql
WITH recent_grades AS (SELECT s."id"   AS  student_id,
                              g."faculty",
                              c."name" AS  course_name,
                              gr."grade",
                              gr."exam_date",
                              ROW_NUMBER() OVER (PARTITION BY s."id", c."id" ORDER BY gr."exam_date" DESC) AS rn
                       FROM postgresql.public."grades" gr
                                JOIN postgresql.public."enrollments" e ON gr."enrollment_id" = e."id"
                                JOIN postgresql.public."students" s ON e."student_id" = s."id"
                                JOIN postgresql.public."groups" g ON s."group_id" = g."id"
                                JOIN postgresql.public."courses" c ON e."course_id" = c."id"
                       WHERE gr."exam_date" >= DATE '2023-01-01'),
     numeric_grades AS (SELECT student_id,
                               faculty,
                               course_name,
                               exam_date,
                               CASE grade
                                   WHEN 'A' THEN 5
                                   WHEN 'B' THEN 4
                                   WHEN 'C' THEN 3
                                   WHEN 'D' THEN 2
                                   WHEN 'F' THEN 1
                                   ELSE NULL
                                   END AS grade_num
                        FROM recent_grades
                        WHERE rn = 1),
     aggregated AS (SELECT faculty,
                           course_name,
                           COUNT(*)       AS    student_count,
                           AVG(grade_num) AS    avg_grade,
                           PERCENTILE_CONT(0.5) WITHIN
GROUP (ORDER BY grade_num) AS median_grade
FROM numeric_grades
GROUP BY faculty, course_name
    )
SELECT faculty,
       course_name,
       student_count,
       avg_grade,
       median_grade,
       CASE
           WHEN avg_grade >= 4.5 THEN 'High performance'
           WHEN avg_grade >= 3 THEN 'Average performance'
           ELSE 'Low performance'
           END AS performance_label
FROM aggregated
ORDER BY faculty, avg_grade DESC;
```

#### Results

| Metric                   | Dremio  | Trino   |
|--------------------------|---------|---------|
| Execution time (1st run) | 6.09 s  | 1.15 s  |
| Execution time (2nd run) | 5.76 s  | 0.71 s  |
| CPU usage (1st run)      | 5.74 s  | 2.69 s  |
| CPU usage (2nd run)      | 5.62 s  | 0.60 s  |
| Max RAM usage (1st run)  | 0.97 MB | 6.83 MB |
| Max RAM usage (2nd run)  | 0.97 MB | 6.84 MB |

### Case 2

#### Query

```sql
WITH student_data AS (SELECT s."id"                                                 AS student_id,
                             s."name"                                               AS student_name,
                             g."name"                                               AS group_name,
                             g."faculty",
                             COUNT(a."id")                                          AS total_attendance,
                             SUM(CASE WHEN a."status" = 'absent' THEN 1 ELSE 0 END) AS absences,
                             ROUND(CAST(AVG(
                                     CASE gr."grade"
                                         WHEN 'A' THEN 5
                                         WHEN 'B' THEN 4
                                         WHEN 'C' THEN 3
                                         WHEN 'D' THEN 2
                                         WHEN 'F' THEN 1
                                         ELSE NULL
                                         END
                                 ) AS DOUBLE), 2)                                   AS avg_exam_score,
                             ROUND(CAST(SUM(sub."score") AS DOUBLE), 2)             AS total_submission_score
                      FROM postgresql.public."students" s
                               JOIN postgresql.public."groups" g ON s."group_id" = g."id"
                               JOIN postgresql.public."enrollments" e ON e."student_id" = s."id"
                               LEFT JOIN postgresql.public."grades" gr ON gr."enrollment_id" = e."id"
                               LEFT JOIN postgresql.public."attendance" a ON a."enrollment_id" = e."id"
                          AND a."date" >= CURRENT_DATE - INTERVAL '90' DAY
                               LEFT JOIN postgresql.public."submissions" sub ON sub."enrollment_id" = e."id"
                          AND sub."submitted_at" >= CURRENT_DATE - INTERVAL '90' DAY
                      GROUP BY s."id", s."name", g."name", g."faculty"),
     ranked_data AS (SELECT *,
                            ROUND(100.0 * absences / NULLIF(total_attendance, 0), 2) AS absence_percent,
                            RANK()                                                      OVER (PARTITION BY group_name ORDER BY total_submission_score DESC) AS activity_rank, COUNT(*) OVER () AS total_students
                     FROM student_data)
SELECT student_id,
       student_name,
       group_name,
       faculty,
       total_attendance,
       absences,
       absence_percent,
       avg_exam_score,
       total_submission_score,
       activity_rank,
       total_students
FROM ranked_data
ORDER BY absence_percent DESC NULLS LAST, activity_rank;
```

#### Results

| Metric                   | Dremio  | Trino  |
|--------------------------|---------|--------|
| Execution time (1st run) | 4.54 s  | 4.21 s |
| Execution time (2nd run) | 4.17 s  | 3.48 s |
| CPU usage (1st run)      | 4.24 s  | 4.67 s |
| CPU usage (2nd run)      | 3.90 s  | 3.45 s |
| Max RAM usage (1st run)  | 1.47 MB | 104 MB |
| Max RAM usage (2nd run)  | 1.47 MB | 104 MB |

## TimescaleDB

### Case 1

#### Query

```sql
WITH sensor_window AS (SELECT "auditorium",
                              "sensor_type",
                              "time",
                              "value",
                              ROW_NUMBER() OVER (PARTITION BY "auditorium", "sensor_type" ORDER BY "time" DESC) AS recent_rank
                       FROM timescale.public."sensor_data"
                       WHERE "time" >= CURRENT_TIMESTAMP - INTERVAL '7' DAY),
     aggregated AS (SELECT "auditorium",
                           "sensor_type",
                           COUNT(*)                      AS measurements,
                           ROUND(AVG("value"), 2)        AS avg_value,
                           MIN("value")                  AS min_value,
                           MAX("value")                  AS max_value,
                           ROUND(STDDEV_POP("value"), 2) AS stddev_value
                    FROM timescale.public."sensor_data"
                    WHERE "time" >= CURRENT_TIMESTAMP - INTERVAL '7' DAY
                    GROUP BY "auditorium", "sensor_type"),
     latest_values AS (SELECT "auditorium",
                              "sensor_type",
                              "value",
                              "time" AS last_time
                       FROM sensor_window
                       WHERE recent_rank = 1)
SELECT a."auditorium",
       a."sensor_type",
       a."measurements",
       a."avg_value",
       a."min_value",
       a."max_value",
       a."stddev_value",
       l."value" AS latest_value,
       l."last_time"
FROM aggregated a
         JOIN latest_values l
              ON a."auditorium" = l."auditorium"
                  AND a."sensor_type" = l."sensor_type"
ORDER BY a."auditorium", a."sensor_type";
```

#### Results

| Metric                   | Dremio  | Trino   |
|--------------------------|---------|---------|
| Execution time (1st run) | 0.37 s  | 1.19 s  |
| Execution time (2nd run) | 0.21 s  | 0.47 s  |
| CPU usage (1st run)      | 0.27 s  | 0.37 s  |
| CPU usage (2nd run)      | 0.12 s  | 0.11 s  |
| Max RAM usage (1st run)  | 1.38 MB | 1.02 MB |
| Max RAM usage (2nd run)  | 1.38 MB | 1.02 MB |

### Case 2

#### Query

```sql
WITH base_data AS (SELECT "auditorium",
                          DATE_TRUNC('hour', "time") AS "hour",
                          "value"
                   FROM timescale.public."sensor_data"
                   WHERE "sensor_type" = 'temperature'),
     hourly_data AS (SELECT "auditorium",
                            "hour",
                            AVG("value")        AS avg_temp,
                            MIN("value")        AS min_temp,
                            MAX("value")        AS max_temp,
                            STDDEV_POP("value") AS stddev_temp
                     FROM base_data
                     GROUP BY "auditorium", "hour"),
     auditorium_avg AS (SELECT "auditorium",
                               AVG(avg_temp)        AS global_avg,
                               STDDEV_POP(avg_temp) AS global_std
                        FROM hourly_data
                        GROUP BY "auditorium")
SELECT h."auditorium",
       h."hour",
       ROUND(h.avg_temp, 2)                                            AS avg_temp,
       ROUND(h.min_temp, 2)                                            AS min_temp,
       ROUND(h.max_temp, 2)                                            AS max_temp,
       ROUND(h.stddev_temp, 2)                                         AS stddev_temp,
       ROUND((h.avg_temp - a.global_avg) / NULLIF(a.global_std, 0), 2) AS z_score
FROM hourly_data h
         JOIN auditorium_avg a
              ON h."auditorium" = a."auditorium"
ORDER BY h."auditorium", h."hour";
```

#### Results

| Metric                   | Dremio  | Trino   |
|--------------------------|---------|---------|
| Execution time (1st run) | 0.70 s  | 1.23 s  |
| Execution time (2nd run) | 0.61 s  | 0.83 s  |
| CPU usage (1st run)      | 0.62 s  | 2.24 s  |
| CPU usage (2nd run)      | 0.56 s  | 0.63 s  |
| Max RAM usage (1st run)  | 1.28 MB | 1.70 MB |
| Max RAM usage (2nd run)  | 1.28 MB | 1.56 MB |

## MongoDB

## Case 1

#### Query

```sql
SELECT "test_id",
       "device",
       COUNT(*)               AS attempts_count,
       ROUND(AVG("score"), 2) AS avg_score
FROM mongo.datvirdb."test_attempts"
GROUP BY "test_id", "device"
ORDER BY "test_id", attempts_count DESC;
```

#### Results

| Metric                   | Dremio  | Trino   |
|--------------------------|---------|---------|
| Execution time (1st run) | 0.38 s  | 0.27 s  |
| Execution time (2nd run) | 0.28 s  | 0.13 s  |
| CPU usage (1st run)      | 0.31 s  | 0.10 s  |
| CPU usage (2nd run)      | 0.24 s  | 0.04 s  |
| Max RAM usage (1st run)  | 6.08 MB | 2.72 KB |
| Max RAM usage (2nd run)  | 6.08 MB | 2.85 KB |

### Case 2

#### Query

```sql
SELECT "survey_id",
       COUNT(*)                     AS total_submissions,
       COUNT(DISTINCT "student_id") AS unique_students
FROM mongo.datvirdb."survey_responses"
GROUP BY "survey_id"
ORDER BY total_submissions DESC;
```

#### Results

| Metric                   | Dremio  | Trino   |
|--------------------------|---------|---------|
| Execution time (1st run) | 0.19 s  | 0.23 s  |
| Execution time (2nd run) | 0.13 s  | 0.11 s  |
| CPU usage (1st run)      | 0.19 s  | 0.08 s  |
| CPU usage (2nd run)      | 0.13 s  | 0.07 s  |
| Max RAM usage (1st run)  | 7.69 MB | 0.28 MB |
| Max RAM usage (2nd run)  | 7.69 MB | 0.28 MB |
