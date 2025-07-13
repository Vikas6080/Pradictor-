import json
import os

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

def handle_feedback(pattern_id, is_correct):
    patterns = load_patterns()
    if pattern_id in patterns:
        if is_correct:
            patterns[pattern_id]["correct"] = patterns[pattern_id].get("correct", 0) + 1
        else:
            patterns[pattern_id]["wrong"] = patterns[pattern_id].get("wrong", 0) + 1
        save_patterns(patterns)
