import pandas as pd
from datetime import datetime, timezone
import os


class CensusDataIngestion:

    def __init__(self):
        self.raw_data_path = "../data/raw/adult.csv"
        self.processed_data_path = "../data/processed/census_data.parquet"

    def load_raw_data(self):
        print("Loading raw data...")
        df = pd.read_csv(self.raw_data_path, skipinitialspace=True)
        print(f"Loaded {len(df)} rows")
        return df

    def clean_data(self, df):
        print("Cleaning data...")
        initial_count = len(df)
        df = df.dropna()
        print(f"Removed {initial_count - len(df)} rows with missing values")

        for col in df.select_dtypes(['object']).columns:
            df[col] = df[col].str.strip()

        return df

    def add_feast_columns(self, df):
        print("Adding Feast columns...")
        df['user_id'] = range(len(df))
        df['event_timestamp'] = datetime.now(timezone.utc)
        return df

    def save_processed_data(self, df):
        print("Saving processed data...")
        os.makedirs(os.path.dirname(self.processed_data_path), exist_ok=True)
        df.to_parquet(self.processed_data_path, index=False)
        file_size = os.path.getsize(self.processed_data_path) / (1024 * 1024)
        print(f"Saved successfully: {self.processed_data_path}")
        print(f"File size: {file_size:.2f} MB")

    def run(self):
        print("=" * 50)
        print("Starting Data Processing")
        print("=" * 50)

        df = self.load_raw_data()
        df = self.clean_data(df)
        df = self.add_feast_columns(df)
        self.save_processed_data(df)

        print("\nData processing completed successfully")
        return df


if __name__ == "__main__":
    ingestion = CensusDataIngestion()
    ingestion.run()