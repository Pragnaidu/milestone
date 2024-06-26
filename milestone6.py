import streamlit as st
import pandas as pd
import os
import requests
import shutil
from io import StringIO

# Get the current working directory
home_dir = os.path.expanduser("~")
os.chdir(home_dir)

# Header
st.markdown("Milestone 3")

# Input box and submit button
url = st.text_input("Enter a URL:")
submit_button = st.button("Submit")

if submit_button:
    # Download the content from the URL and save it to a local file
    home_dir = os.path.expanduser("~")
    input_dir = os.path.join(home_dir, "Downloads")
    os.makedirs(input_dir, exist_ok=True)

    inputFile = os.path.join(input_dir, f"{url.split('/')[-1]}")
    response = requests.get(url, allow_redirects=False)
    direct_download_url = response.headers['Location']
    response = requests.get(direct_download_url, stream=True)
    with open(inputFile, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    text_df = pd.read_csv(inputFile)
    #text_df = pd.read_csv(StringIO(text_data))

    # Load the data from the other local files
    
    #csv_dir = os.path.join(home_dir, "Documents" , "Milestone3Files")
    # Change the working directory to the one where the CSV files are located
    #os.chdir(csv_dir)
    # Load the data from the other local files
    # Load the data from the other GitHub files
    csv_url1 = "https://raw.githubusercontent.com/Pragnaidu/milestone/main/liveCustomerList.csv"
    csv_url2 = "https://raw.githubusercontent.com/Pragnaidu/milestone/main/liveBankAcct.csv"
    csv_df1 = pd.read_csv(csv_url1)
    csv_df2 = pd.read_csv(csv_url2)

    #csv_df1 = pd.read_csv("liveCustomerList.csv")
    #csv_df2 = pd.read_csv("liveBankAcct.csv")
    
    # Merge the data from the different files
    merged_df1 = pd.merge(text_df, csv_df1[['custID', 'firstName', 'lastName']], on='custID', how='left')
    merged_df2 = pd.merge(text_df, csv_df2[['bankAcctID', 'firstName', 'lastName']], left_on='loginAcct', right_on='bankAcctID', how='left')

    # Create a new dataframe with custID and rightAcctFlag
    output_df = pd.DataFrame(columns=['custID', 'rightAcctFlag'])
    output_df['custID'] = merged_df1['custID']
    output_df['rightAcctFlag'] = ((merged_df1['firstName'] == merged_df2['firstName']) & (merged_df1['lastName'] == merged_df2['lastName'])).astype(int)
    
    
    download_button = st.download_button(
        label="Download File",
        data=output_df.to_csv(index=False),
        file_name=f"{url.split('/')[-1].split('.')[0]}.csv",
        mime="text/csv"
    )
