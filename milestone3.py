from os import makedirs
import pandas as pd
import requests
import shutil
import os


url = "https://www.dropbox.com/scl/fi/izr34r20y498f5lvn3d9f/2203227.csv?rlkey=f30ceawbf4b23ggb8tccvd3ka&dl=1"
inputFile = os.path.join(os.path.expanduser('~'), "Downloads", "dropBoxFile.csv")
outputDir = os.path.join(os.path.expanduser('~'), "Downloads", "py" , "dropbox3")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(inputFile, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
makedirs(outputDir, exist_ok=True)

text_file_path = "/Users/pragnaboyallaramamurthy/Downloads/dropBoxFile.csv"
'''text_df = pd.read_csv(text_file_path, sep=',')'''
text_df = pd.read_csv(text_file_path)
csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone3Files/liveCustomerList.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone3Files/liveBankAcct.csv"
csv_df1 = pd.read_csv(csv_file1_path)
csv_df2 = pd.read_csv(csv_file2_path)
merged_df1 = pd.merge(text_df, csv_df1[['custID', 'firstName', 'lastName']], on='custID', how='left')
merged_df2 = pd.merge(text_df, csv_df2[['bankAcctID', 'firstName', 'lastName']], left_on='loginAcct' , right_on='bankAcctID' , how='left')
merged_df1.rename(columns={'firstName': 'firstName_x', 'lastName': 'lastName_x'}, inplace=True)
merged_df2.rename(columns={'firstName': 'firstName_y', 'lastName': 'lastName_y'}, inplace=True)
merged_df1['rightAcctFlag'] = merged_df1.apply(lambda row: 1 if row['firstName_x'] == row['firstName_y'] and row['lastName_x'] == row['lastName_y'] else 0, axis=1)
output_df = merged_df1[['custID', 'rightAcctFlag']]
filename = url.split('/')[-1].split('.')[0]
output_csv_file = f"/Users/pragnaboyallaramamurthy/Downloads/py/{filename}.csv"
output_df.to_csv(output_csv_file, index=False)

