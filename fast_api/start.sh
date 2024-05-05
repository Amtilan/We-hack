#!/bin/bash

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
