#!/bin/bash

echo "Installing requirements..."
pip install -r requirements.txt

echo "Starting FastAPI server..."
uvicorn app.main:app --reload