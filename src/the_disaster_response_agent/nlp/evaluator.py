import json
import random
from the_disaster_response_agent.nlp.extractor import extract_from_text

def evaluate_on_humaid(path: str, n: int = 30, seed: int = 42):
    with open(path) as f:
        lines = [json.loads(line) for line in f]

    random.seed(seed)
    sample = random.sample(lines, n)

    correct = 0
    mismatches = []
    for line in sample:
        predicted = extract_from_text(line["text"])
        actual = line["humanitarian_category"]
        match = predicted.humanitarian_category == actual
        correct += match
        if not match:
            mismatches.append((line["text"], predicted.humanitarian_category, actual))
        print(f"Predicted: {str(predicted.humanitarian_category):35} | Actual: {actual:35} | Match: {match}")

    print(f"\nAccuracy on {n} random samples: {correct}/{n} ({100*correct/n:.1f}%)")

    if mismatches:
        print("\n--- Mismatches ---")
        for text, pred, actual in mismatches:
            print(f"Text: {text}\n  Predicted: {pred} | Actual: {actual}\n")

if __name__ == "__main__":
    evaluate_on_humaid("data/processed/humaid_train.jsonl")