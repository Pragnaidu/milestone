import os
import requests
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

url = "https://www.dropbox.com/scl/fi/dg5qe0s75hkf5k2j2rvzz/3104854.csv?rlkey=abml9n1tbcgi00w516owfuzgy&dl=1"
inputFile = os.path.join(os.path.expanduser('~'), "Downloads", "py" , "dropbox4.csv")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(inputFile, 'wb') as out_file:
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
union_df['date'] = pd.to_datetime(union_df['date'])

eodBalance = union_df.groupby(['date','bankAcctID']).sum('transAmount').reset_index()
eodBalance['balance'] = eodBalance.groupby('bankAcctID')['transAmount'].cumsum()
eodBalance['date'] = pd.to_datetime(eodBalance['date'])
eobBalance = eodBalance[(eodBalance['date'] >= '2020-03-01') & (eodBalance['date'] <= '2020-04-30')]
output_csv_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4csv.csv"
eobBalance.to_csv(output_csv_path, index=False)
eob_csv = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4csv.csv"
eobBalance = pd.read_csv(eob_csv)

output_pdf_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4"
plt.figure(figsize=(12, 6))
for bankAcctID in eobBalance['bankAcctID'].unique():
    bankAcctData = eobBalance[eobBalance['bankAcctID'] == bankAcctID]
    date_values = np.array([np.datetime64(x) for x in bankAcctData['date']])
    balance_values = np.array(bankAcctData['balance'], dtype=np.float64)
    plt.step(date_values, balance_values, label=f"Bank Account {bankAcctID}", where='post')
plt.title("EOD Balance for Bank Account " + str(bankAcctID))
plt.xlabel("Date")
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
plt.ylabel("Balance")
plt.legend()
plt.grid()
filename = url.split('/')[-1].split('.')[0]
plt.savefig(os.path.join(output_pdf_path, f'{filename}.pdf'))
plt.show()

'''
filtered_data = eobBalance[eobBalance['balance'] >= 200] 
filtered_df = filtered_data.groupby('bankAcctID').max().reset_index()
plt.figure(figsize=(12, 6))
plt.bar(filtered_df['bankAcctID'], filtered_df['balance'], label='Amount >= 200', alpha=0.5) 
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.ylabel("Balance") 
plt.legend()
plt.grid()
plt.show()
'''