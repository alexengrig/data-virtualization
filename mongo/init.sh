#!/bin/bash

echo "Waiting for MongoDB to start..."
sleep 5

mongoimport --db datvirdb --collection test_attempts --file /docker-entrypoint-initdb.d/data/test_attempts.json --batchSize 1000
mongoimport --db datvirdb --collection survey_responses --file /docker-entrypoint-initdb.d/data/survey_responses.json --batchSize 1000
