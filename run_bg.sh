#!/usr/bin/env bash
source "./.venv/bin/activate"
pip install -r requirements.txt
python3 background_script.py
deactivate