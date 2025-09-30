#!/bin/sh

while ! nc -z db 5432; do
  echo "Waiting for db..."
  sleep 1
done

python api.py
