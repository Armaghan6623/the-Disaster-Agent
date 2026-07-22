from transformers import pipeline
from typing import Dict, Any


class DisasterResponseAgent:
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        self.model_name = model_name
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            return_all_scores=True
        )

    def assess_incident(self, text: str) -> Dict[str, Any]:
        """Assess disaster severity and category from incident text."""
        result = self.classifier(text)
        return {
            "text": text,
            "assessment": result[0] if result else None,
            "severity": self._extract_severity(result[0] if result else [])
        }

    def _extract_severity(self, scores: list) -> str:
        """Extract severity classification from model scores."""
        if not scores:
            return "unknown"
        top = max(scores, key=lambda x: x["score"])
        return top.get("label", "unknown").lower()