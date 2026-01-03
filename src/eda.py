# src/eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, file_path):
        """Load CFPB complaints dataset"""
        self.df = pd.read_csv(file_path)

    def product_distribution(self):
        """Plot distribution of complaints across products"""
        plt.figure(figsize=(10,6))
        sns.countplot(data=self.df, y='Product', order=self.df['Product'].value_counts().index)
        plt.title("Number of Complaints per Product")
        plt.xlabel("Count")
        plt.ylabel("Product")
        plt.show()

    def narrative_length_analysis(self):
        """Calculate word count of narratives and visualize distribution"""
        self.df['narrative_length'] = self.df['Consumer complaint narrative'].fillna("").apply(lambda x: len(str(x).split()))
        print("Narrative Length Statistics:")
        print(self.df['narrative_length'].describe())

        plt.figure(figsize=(10,6))
        sns.histplot(self.df['narrative_length'], bins=50, kde=True)
        plt.title("Distribution of Consumer Complaint Narrative Lengths")
        plt.xlabel("Word Count")
        plt.ylabel("Frequency")
        plt.show()

    def missing_narratives(self):
        """Count number of complaints with and without narratives"""
        missing_count = self.df['Consumer complaint narrative'].isna().sum()
        total_count = len(self.df)
        print(f"Complaints with missing narratives: {missing_count}")
        print(f"Complaints with narratives: {total_count - missing_count}")
