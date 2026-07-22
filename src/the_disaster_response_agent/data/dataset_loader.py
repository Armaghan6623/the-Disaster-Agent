import json
from pathlib import Path
from datasets import load_dataset
from the_disaster_response_agent.data.adapters.humaid_adapter import adapt_humaid_row
from the_disaster_response_agent.data.preprocessor import clean_tweet_text

PROCESSED_DIR = Path("data/processed")

def load_and_process_humaid(split: str = "train") -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    dataset = load_dataset(
        "QCRI/HumAID-all",
        split=split,
        verification_mode="no_checks",
    )

    output_path = PROCESSED_DIR / f"humaid_{split}.jsonl"
    with open(output_path, "w") as f:
        for row in dataset:
            row["tweet_text"] = clean_tweet_text(row["tweet_text"])
            event = adapt_humaid_row(row)
            f.write(json.dumps(event.__dict__) + "\n")

    print(f"Processed {len(dataset)} rows -> {output_path}")


def load_disaster_dataset(split: str = "train") -> None:
    return load_and_process_humaid(split)


if __name__ == "__main__":
    load_and_process_humaid("train")