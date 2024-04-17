from zipfile import ZipFile
from os import makedirs
import pandas as pd
import requests
import shutil
import os
import csv


url = "https://www.dropbox.com/scl/fi/4zhh24vyt9i011vf43yq5/2172120.zip?rlkey=vfi1xit6s2lwesu9ntwiz1yj1&dl=1"
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
csv_file_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/jpegnames.csv"
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['custID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for filename in jpeg_files:
        writer.writerow({'custID': filename})


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/jpegnames.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/Milestone2Files/liveCustomerList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
merged_df = pd.merge(df1, df2, on='custID', how='inner')
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/joined.csv"
merged_df.to_csv(output_csv_file, index=False)
print("Join operation completed. Merged CSV file saved as:", output_csv_file)


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/joined.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/Milestone2Files/liveFraudList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df1['lastName'] = df1['lastName'].str.lower()
df2['lastName'] = df2['lastName'].str.lower()
merged_df = pd.merge(df1, df2, on='lastName', how='inner')
output_df = merged_df[['custID']]
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/fraudster.csv"
output_df.to_csv(output_csv_file, index=False)


csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/jpegnames.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/fraudster.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
merged_df = pd.merge(df1, df2, on='custID', how='left')

# Create a new column 'fraudster' and initialize it to 0
merged_df['fraudster'] = 0

# Set 'fraudster' to 1 for custIDs present in the second CSV
merged_df.loc[merged_df['custID'].isin(df2['custID']), 'fraudster'] = 1

# Save the merged DataFrame to a new CSV file
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/Allfraudster.csv" 
merged_df.to_csv(output_csv_file, index=False)

print("Merged CSV file saved as:", output_csv_file)
'''
csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/joined.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/Milestone2Files/liveFraudList.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df1['lastName'] = df1['lastName'].str.lower()
df2['lastName'] = df2['lastName'].str.lower()
merged_df = pd.merge(df1, df2, on='lastName', how='inner')
merged_df['fraudster'] = 1
output_df = merged_df[['custID', 'lastName', 'fraudster']]
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/fraudster.csv"
output_df.to_csv(output_csv_file, index=False)
print("Filtered and selected columns. CSV file saved as:", output_csv_file)
'''


''' 
csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/Milestone2Files/liveFraudList.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/fraudster.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
merged_df = pd.merge(df1, df2, on='lastName', how='left')
output_df = merged_df[['custID','fraudster']]
output_csv_file = "/Users/pragnaboyallaramamurthy/Downloads/projectpossible/Allfraudster.csv" 
output_df.to_csv(output_csv_file, index=False)   
'''


