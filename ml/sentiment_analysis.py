"""
WatchSphere AI v3.0 - NLP Review Sentiment Analysis Engine
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import re
from typing import Dict, Any


class SentimentAnalysisEngine:
    """
    NLP sentiment text classifier analyzing review text into Positive, Neutral, Negative.
    """

    POSITIVE_WORDS = {"excellent", "amazing", "great", "best", "love", "outstanding", "superb", "quality", "fast", "perfect"}
    NEGATIVE_WORDS = {"bad", "poor", "terrible", "horrible", "worst", "defective", "broken", "slow", "disappointed", "refund"}

    @classmethod
    def analyze_text(cls, text: str) -> Dict[str, Any]:
        """Classifies text sentiment and extracts emotion confidence."""
        if not text:
            return {"sentiment": "Neutral", "confidence": 0.50, "score": 0.0}

        cleaned = re.sub(r"[^\w\s]", "", text.lower())
        words = set(cleaned.split())

        pos_count = len(words.intersection(cls.POSITIVE_WORDS))
        neg_count = len(words.intersection(cls.NEGATIVE_WORDS))

        if pos_count > neg_count:
            sentiment = "Positive"
            confidence = min(0.98, 0.75 + (pos_count * 0.08))
            score = 0.85
        elif neg_count > pos_count:
            sentiment = "Negative"
            confidence = min(0.98, 0.75 + (neg_count * 0.08))
            score = -0.85
        else:
            sentiment = "Neutral"
            confidence = 0.65
            score = 0.0

        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2),
            "score": score,
            "keywords": list(words.intersection(cls.POSITIVE_WORDS.union(cls.NEGATIVE_WORDS)))
        }
