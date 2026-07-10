import os
import pandas as pd

print("Downloading dataset...")

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
]

os.makedirs('../data', exist_ok=True)
df = pd.read_csv(url, names=columns, na_values=' ?', skipinitialspace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('../data/adult.csv', index=False)

print(f"Downloaded to: ../data/adult.csv")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")