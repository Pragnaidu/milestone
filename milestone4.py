import os
import requests
import shutil
import pandas as pd
import matplotlib.pyplot as plt

url = "https://www.dropbox.com/scl/fi/3p1ekhrd232rf2qgb7ehr/2265155.csv?rlkey=n4sxmtf01ck1m9ewz9j3ss58h&dl=1"
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
grouped_df['balance'] = grouped_df.groupby('bankAcctID')['transAmount'].cumsum()
grouped_df.loc[grouped_df['transAmount'] < 0, 'balance'] -= grouped_df.loc[grouped_df['transAmount'] < 0, 'transAmount'].abs()

filtered_date_df = grouped_df[(grouped_df['date'] >= '2020-03-01') & (grouped_df['date'] <= '2020-04-30')]
plt.figure(figsize=(10, 6))
plt.plot(filtered_date_df['date'], filtered_date_df['balance'], linestyle='-')
plt.title('Transaction Amount Over Time')
plt.xlabel('Date')
plt.ylabel('EOB')
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
output_pdf_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4"
filename = url.split('/')[-1].split('.')[0]
plt.savefig(os.path.join(output_pdf_path, f'{filename}.pdf'))
plt.show()