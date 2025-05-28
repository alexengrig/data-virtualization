CREATE TABLE sensor_data
(
    time        TIMESTAMPTZ   NOT NULL,
    auditorium  TEXT          NOT NULL,
    sensor_type TEXT          NOT NULL,
    value       NUMERIC(6, 2) NOT NULL
);
