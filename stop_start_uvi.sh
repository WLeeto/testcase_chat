#!/bin/bash

PID=$(lsof -t -i:8000)
if [ -n "$PID" ]; then
  echo "Stopping existing uvicorn process (PID $PID)..."
  kill $PID
  sleep 1
fi

echo "Starting uvicorn..."
uvicorn main:app --reload &