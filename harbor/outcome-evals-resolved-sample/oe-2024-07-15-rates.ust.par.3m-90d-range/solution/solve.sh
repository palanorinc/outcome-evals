#!/bin/bash
# Fixed-answer baseline: the same answer for every question; no model.
echo '{"probability": 0.5}' > /app/answer.json
