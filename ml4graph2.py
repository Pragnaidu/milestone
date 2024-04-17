import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('/Users/pragnaboyallaramamurthy/Downloads/py/dropbox4csv.csv')

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter the DataFrame to only include rows where the balance is greater than 200
filtered_df = df[df['transAmount'] > 200]

# Get the unique bankAcctID values
bankAcctIDs = filtered_df['bankAcctID'].unique()

# Create a figure with a grid of subplots
fig, axs = plt.subplots(nrows=len(bankAcctIDs), figsize=(12, 6))

# Define a list of colors for each account
colors = ['b', 'g', 'r']

# Loop through each unique bankAcctID and plot a bar for each one
for i, bankAcctID in enumerate(bankAcctIDs):
    data = filtered_df[filtered_df['bankAcctID'] == bankAcctID]
    axs[i].bar(data['date'], data['transAmount'], label=bankAcctID, color=colors[i % len(colors)])
    axs[i].set_title(f"Bank Account {bankAcctID}")
    axs[i].set_xlabel("Date")
    axs[i].set_ylabel("Amount")
    axs[i].legend()
    axs[i].xaxis_date()
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axs[i].xaxis.set_major_locator(mdates.DayLocator(interval=15))
    axs[i].tick_params(axis='x', rotation=45)
    axs[i].set_yticks(np.arange(0, 1001, 500))
    for p in axs[i].patches:
        axs[i].annotate(format(p.get_height(), '.0f'),
                         xy=(p.get_x() + p.get_width() / 2, p.get_height()),
                         xytext=(0, 3),
                         textcoords='offset points',
                         ha='center', va='bottom')

# Set the overall figure title and tighten the layout
plt.suptitle("Bank Account Balances Greater Than 200")
plt.tight_layout()

# Show the plot
plt.show()