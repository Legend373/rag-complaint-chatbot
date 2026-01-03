import pandas as pd
import re

class Preprocessor:
    def __init__(self, df):
        """Initialize with a DataFrame"""
        self.df = df.copy()

    def filter_products(self, products_list):
        """Filter dataset to include only specified products"""
        self.df = self.df[self.df['Product'].isin(products_list)]
        return self

    def remove_empty_narratives(self):
        """Remove rows with empty or NaN narratives"""
        self.df = self.df.dropna(subset=['Consumer complaint narrative'])
        self.df = self.df[self.df['Consumer complaint narrative'].str.strip() != '']
        return self

    @staticmethod
    def clean_text(text):
        """Fully clean consumer complaint narrative for embeddings"""
        text = str(text).lower()

        # Remove byte-string prefix (b' or b")
        text = re.sub(r"^b['\"]", "", text)

        # Remove boilerplate phrases
        boilerplate_patterns = [
            r"i am writing to file a complaint",
            r"i am writing to complain",
            r"this is a complaint about",
            r"dear cfpb",
            r"b'i am writing to dispute",
            r"b'i am writing",
            r"i am writing"
        ]
        for pattern in boilerplate_patterns:
            text = re.sub(pattern, "", text)

        # Remove special characters (keep only letters, numbers, spaces)
        text = re.sub(r"[^a-z0-9\s]", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def preprocess_narratives(self):
        """Apply text cleaning to all narratives"""
        self.df['cleaned_narrative'] = self.df['Consumer complaint narrative'].apply(self.clean_text)

        # Remove rows that became empty after cleaning
        self.df = self.df[self.df['cleaned_narrative'].str.strip() != '']

        return self

    def get_df(self):
        """Return processed DataFrame"""
        return self.df
