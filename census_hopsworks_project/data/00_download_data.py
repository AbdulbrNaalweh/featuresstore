import urllib.request
import os

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
output_path = "../data/adult.csv"

print("Downloading dataset...")
urllib.request.urlretrieve(url, output_path)

column_names = "age,workclass,fnlwgt,education,education_num,marital_status,occupation,relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,income\n"

with open(output_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(column_names + content)

print(f"Downloaded to: {output_path}")