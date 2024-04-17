import os
import requests
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

url = "https://www.dropbox.com/scl/fi/ept339r0ttsa8uqdfg82s/2214829.csv?rlkey=dh151vymi1qdsyekzs902vv0k&dl=1"
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

bank_acct_ids = df1['bankAcctID']
union_df = pd.concat([df2, df3])
filtered_df = union_df[union_df['bankAcctID'].isin(bank_acct_ids)]

grouped_df = filtered_df.groupby(['bankAcctID', 'date']).sum().reset_index()
print(grouped_df)
grouped_df['balance'] = grouped_df.groupby('bankAcctID')['transAmount'].cumsum()

grouped_df.loc[grouped_df['transAmount'] < 0, 'balance'] -= grouped_df.loc[grouped_df['transAmount'] < 0, 'transAmount'].abs()


# Calculate the EODBalance for each bankAcctID and date
EODBal = filtered_df.groupby(['date', 'bankAcctID']).sum().reset_index()
EODBal = EODBal.rename(columns={'transAmount': 'EODBalance'})


# Calculate the cumulative sum of EODBalance for each bankAcctID
EODBalCum = EODBal.groupby('bankAcctID').cumsum()

# Merge the EODBal and EODBalCum dataframes on 'bankAcctID' and 'date'
result = pd.merge(EODBal, EODBalCum, on=['bankAcctID', 'date'])


filtered_date_df = grouped_df[(grouped_df['date'] >= '2020-03-01') & (grouped_df['date'] <= '2020-04-30')]
filtered_date_df['date'] = pd.to_datetime(filtered_date_df['date']).sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
for bank_acct_id in bank_acct_ids:
    temp_df = filtered_date_df[filtered_date_df['bankAcctID'] == bank_acct_id]
    ax.step(temp_df['date'], temp_df['balance'], linestyle='-')
ax.set_title('Transaction Amount Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('EOB')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.grid(True)
ax.legend(bank_acct_ids)
plt.tight_layout()
output_pdf_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4"
filename = url.split('/')[-1].split('.')[0]
plt.savefig(os.path.join(output_pdf_path, f'{filename}.pdf'))
plt.show()

    
    
    
    
    
    
    
    
    