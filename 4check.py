import os
import requests
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

url = "https://www.dropbox.com/scl/fi/st03eewt8tenumdkpbz9c/2285023.csv?rlkey=r0yv3sxprc884vepx8ccfdvfy&dl=1"
input_file = os.path.join(os.path.expanduser('~'), "Downloads", "py" , "dropbox4.csv")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(input_file, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone4Files/startBalance.csv"
csv_file3_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone4Files/bankTransactions.csv"
df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df2 = df2.rename(columns={'amt': 'transAmount'})
df3 = pd.read_csv(csv_file3_path)

# Perform a left join between df1 and union_df based on 'bankAcctID'
merged_df1 = pd.merge(df1, df2, how='left', on='bankAcctID')
merged_df2 = pd.merge(df1, df3, how ='left' , on='bankAcctID')

union_df = pd.concat([merged_df1, merged_df2], ignore_index=True)
union_df['uniqueID'] = union_df['bankAcctID'].astype(str) + '_' + union_df['date'].dt.strftime('%Y-%m-%d')
print(union_df)