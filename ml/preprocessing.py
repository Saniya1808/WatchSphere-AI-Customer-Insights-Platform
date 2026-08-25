"""
WatchSphere AI v3.0 - ML Data Preprocessing Pipeline
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer


class MLPreprocessingPipeline:
    """
    Data cleaning, scaling, vectorization, and feature engineering utilities.
    """

    @staticmethod
    def scale_features(df: pd.DataFrame, feature_cols: list) -> np.ndarray:
        """Scales numerical feature columns using StandardScaler."""
        if df.empty:
            return np.array([])
        scaler = StandardScaler()
        return scaler.fit_transform(df[feature_cols].fillna(0))

    @staticmethod
    def tfidf_vectorize(text_list: list, max_features: int = 100) -> np.ndarray:
        """Converts raw review text into TF-IDF numerical matrix."""
        if not text_list:
            return np.array([])
        vectorizer = TfidfVectorizer(max_features=max_features, stop_words="english")
        return vectorizer.fit_transform(text_list).toarray()
