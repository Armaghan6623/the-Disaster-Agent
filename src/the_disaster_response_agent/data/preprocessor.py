import re

def clean_tweet_text(text: str) -> str:
    """Basic cleanup for HumAID tweet text."""
    text = re.sub(r"^RT\s+@\w+:\s*", "", text)   # strip leading retweet handle
    text = re.sub(r"\s+", " ", text).strip()      # collapse whitespace
    return text