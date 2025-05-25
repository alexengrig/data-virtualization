COPY sensor_data(time, auditorium, sensor_type, value)
    FROM '/docker-entrypoint-initdb.d/data/sensor_data.csv' DELIMITER ',' CSV;
