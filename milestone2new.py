from zipfile import ZipFile
from os import makedirs
import pandas as pd
import requests
import shutil
import os
import csv


url = "https://www.dropbox.com/scl/fi/biuxg7f6plgu4owicziqf/2212088.zip?rlkey=6kd2yio06hvmaaaevlsk9wne5&dl=1"
inputFile = os.path.join(os.path.expanduser('~'), "Downloads", "dropBoxFile.zip")
outputDir = os.path.join(os.path.expanduser('~'), "Downloads", "dropbox")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(inputFile, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
makedirs(outputDir, exist_ok=True)
with ZipFile(inputFile) as zipObj:
    zipObj.extractall(outputDir)
    

image_directory = "/Users/pragnaboyallaramamurthy/Downloads/dropbox"
jpeg_files = []
for filename in os.listdir(image_directory):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        jpeg_files.append(os.path.splitext(filename)[0])
csv_file_path = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/jpegnames.csv"
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['custID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for filename in jpeg_files:
        writer.writerow({'custID': filename})


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/jpegnames.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone2Files/liveCustomerList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
merged_df = pd.merge(df1, df2, on='custID', how='inner')
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/joined.csv"
merged_df.to_csv(output_csv_file, index=False)
print("Join operation completed. Merged CSV file saved as:", output_csv_file)


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/joined.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone2Files/liveFraudList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df1['lastName'] = df1['lastName'].str.lower()
df2['lastName'] = df2['lastName'].str.lower()
merged_df = pd.merge(df1, df2, on='lastName', how='inner')
output_df = merged_df[['custID']]
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/fraudster.csv"
output_df.to_csv(output_csv_file, index=False)


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/joined.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone2Files/liveFraudList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df1['lastName'] = df1['lastName'].str.lower()
df2['lastName'] = df2['lastName'].str.lower()
merged_df = pd.merge(df1, df2, on='lastName', how='left', indicator=True)
merged_df['fraudster'] = merged_df['_merge'].apply(lambda x: 1 if x == 'both' else 0)
merged_df.drop(columns=['_merge'], inplace=True)
output_df = merged_df[['custID', 'fraudster']]
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/py/projectpossible/fraudster.csv"
output_df.to_csv(output_csv_file, index=False)
print("Filtered and selected columns. CSV file saved as:", output_csv_file)







