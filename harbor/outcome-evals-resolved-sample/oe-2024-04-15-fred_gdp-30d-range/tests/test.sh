#!/bin/bash
set -u
mkdir -p /logs/verifier
python3 /tests/grade.py /app/answer.json /tests/resolution.json /logs/verifier
