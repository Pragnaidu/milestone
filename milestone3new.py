import pandas as pd
import os
import requests
import shutil

url = "https://www.dropbox.com/scl/fi/p4qmdsfncadin8sdec4dg/362563.csv?rlkey=ok3pzi8kffnzczqzyclz74oln&dl=1"
inputFile = os.path.join(os.path.expanduser('~'), "Downloads", "dropBoxFile.csv")
outputDir = os.path.join(os.path.expanduser('~'), "Downloads", "py" , "dropbox3")
response = requests.get(url, allow_redirects=False)
direct_download_url = response.headers['Location']
response = requests.get(direct_download_url, stream=True)
with open(inputFile, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

text_df = pd.read_csv(inputFile)
csv_df1 = pd.read_csv("/Users/pragnaboyallaramamurthy/Downloads/py/Milestone3Files/liveCustomerList.csv")
csv_df2 = pd.read_csv("/Users/pragnaboyallaramamurthy/Downloads/py/Milestone3Files/liveBankAcct.csv")

merged_df1 = pd.merge(text_df, csv_df1[['custID', 'firstName', 'lastName']], on='custID', how='left')
merged_df2 = pd.merge(text_df, csv_df2[['bankAcctID', 'firstName', 'lastName']], left_on='loginAcct', right_on='bankAcctID', how='left')

# Create a new dataframe with custID and rightAcctFlag
output_df = pd.DataFrame(columns=['custID', 'rightAcctFlag'])
output_df['custID'] = merged_df1['custID']
output_df['rightAcctFlag'] = ((merged_df1['firstName'] == merged_df2['firstName']) & (merged_df1['lastName'] == merged_df2['lastName'])).astype(int)
filename = url.split('/')[-1].split('.')[0]
output_csv_file = f"/Users/pragnaboyallaramamurthy/Downloads/py/{filename}.csv"
output_df.to_csv(output_csv_file, index=False)

