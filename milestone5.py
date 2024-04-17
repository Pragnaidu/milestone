import pandas as pd
import requests
import os
import datetime
import shutil


# Downloading files from Dropbox
url = "https://www.dropbox.com/scl/fi/tfyvwbsh4fjktpj4noq8j/4177457.csv?rlkey=ehaxbgci9zhcrz434oxiws3z0&dl=1"
inputFile = os.path.join(os.path.expanduser('~'), "Downloads", "py", "dropbox5.csv")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(inputFile, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# Reading CSV files
csv_file1_path = "/Users/pragnaboyallaramamurthy/Downloads/py/dropbox5.csv"
csv_file2_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone5Files/startBalance.csv"
csv_file3_path = "/Users/pragnaboyallaramamurthy/Downloads/py/Milestone5Files/bankTransactions.csv"

df1 = pd.read_csv(csv_file1_path)
df2 = pd.read_csv(csv_file2_path)
df3 = pd.read_csv(csv_file3_path)

# Merging DataFrames
# Merging DataFrames
startbal_acct = pd.merge(df1, df2, how='left', on='bankAcctID')
transactions_acct = pd.merge(df1, df3, how='left', on='bankAcctID')

transactions_acct = transactions_acct.rename(columns={"transAmount": "amt"})

bal_transactions = pd.concat([startbal_acct, transactions_acct])

salary_data = bal_transactions[bal_transactions["amt"] > 200].sort_values(by="bankAcctID")
salary_filterdata = salary_data[(salary_data["date"] >= "2020-01-01") & (salary_data["date"] <= "2020-04-30")]
salary_filterdata["date"] = pd.to_datetime(salary_filterdata["date"])
salary_filterdata["day_of_week"] = salary_filterdata["date"].dt.day_name()

salary_groupeddata = salary_filterdata.groupby("bankAcctID").apply(lambda x: x.sort_values("date")).reset_index(drop=True)
lastTwoTransactions = salary_groupeddata.groupby("bankAcctID").tail(2)
paydate_diff = lastTwoTransactions.groupby("bankAcctID").apply(lambda x: (x["date"].iloc[-1] - x["date"].iloc[-2]).days).rename("predicted")

salary_filterdata.loc[:, "date"] = pd.to_datetime(salary_filterdata["date"])
grouped_data = salary_filterdata.groupby("bankAcctID", group_keys=False).apply(lambda x: x.sort_values("date", ascending=False)).reset_index(drop=True)
latest_dates = grouped_data.groupby("bankAcctID").head(1)

merged_data = pd.merge(latest_dates, paydate_diff, on="bankAcctID")
merged_data["date"] = merged_data["date"] + pd.to_timedelta(merged_data["predicted"], unit="D")
merged_data["predicted_day_of_week"] = merged_data["date"].dt.day_name()

merged_data["date"] = merged_data["date"].apply(lambda x: x - datetime.timedelta(days=x.weekday()) if x.weekday() >= 5 else x)
merged_data["predicted_day_of_week"] = merged_data["date"].dt.day_name()

results_ms5 = merged_data[["bankAcctID", "date"]]

filename = url.split('/')[-1].split('.')[0]
output_csv_file = os.path.join(os.path.expanduser('~'), "Downloads", "py", f"{filename}.csv")
results_ms5[['bankAcctID', 'date']].to_csv(output_csv_file, index=False)

