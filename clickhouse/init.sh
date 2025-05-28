#!/bin/bash
clickhouse-client --multiquery < /docker-entrypoint-initdb.d/01_schema.sql
clickhouse-client --query="INSERT INTO platform_events FORMAT CSV" < /docker-entrypoint-initdb.d/data/platform_events.csv
clickhouse-client --query="INSERT INTO teaching_summary FORMAT CSV" < /docker-entrypoint-initdb.d/data/teaching_summary.csv
