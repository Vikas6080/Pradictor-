import json
import random
import os
from hashlib import sha256

DATA_FILE = "data/patterns.json"

def load_patterns():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_patterns(patterns):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(patterns, f, indent=2)

def hash_board(board):
    flat = [cell.strip().upper() for row in board for cell in row]
    flat_str = ",".join(flat)
    return sha256(flat_str.encode()).hexdigest()[:12]  # Shorter ID

def predict_safe_cells(board):
    pattern_id = hash_board(board)
    patterns = load_patterns()

    if pattern_id in patterns:
        data = patterns[pattern_id]
        safe = data.get("safe_cells", [])
    else:
        # If unseen pattern, randomly select 3 cells
        all_cells = [chr(65 + r) + str(c + 1) for r in range(5) for c in range(5)]
        safe = random.sample(all_cells, 3)
        patterns[pattern_id] = {"safe_cells": safe, "correct": 0, "wrong": 0}
        save_patterns(patterns)

    return safe, pattern_id
