from the_disaster_response_agent.data.schema import DisasterEvent

def adapt_humaid_row(row: dict) -> DisasterEvent:
    return DisasterEvent(
        text=row["tweet_text"],
        source="humaid",
        humanitarian_category=row["class_label"],
        raw_metadata=row,
    )