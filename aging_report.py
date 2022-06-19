# Import modules
from matplotlib.pyplot import margins
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

# Load data
xlsx = r"C:\Users\mfaraday01\Documents\Code\fifo_aging_analysis\fifo_aging_analysis\prefinance.xlsx"
df = pd.read_excel (xlsx, 
                     sheet_name="Debits"
                     )
credit = pd.read_excel (xlsx, 
                     sheet_name="Credit"
                     )

# Unipivot df df
df = df.melt(id_vars=["Name"], var_name="Date", value_name="Amount")

# Change datatypes
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Add new calculated columns

df["Due date"] = df["Date"] + timedelta(days=7)
df["Overdue"] = (datetime.date(datetime.now()) - df["Due date"]).dt.days.astype('int16')

# Categorize overdue time to ages

conditions = [
               (df["Overdue"] <= 7),
               (df["Overdue"] > 7) & (df["Overdue"] <= 14),
               (df["Overdue"] > 14) & (df["Overdue"] <= 21),
               (df["Overdue"] > 21) & (df["Overdue"] <= 60),
               (df["Overdue"] > 60) & (df["Overdue"] <= 120),
               (df["Overdue"] > 120) & (df["Overdue"] <= 180),
               (df["Overdue"] > 180)               
               ]

choices = [
            "1-7 days",
            "8-15 days",
            "16-21 days",
            "22-60 days",
            "61-120 days",
            "121-180 days",
            "Above 180"
            ]

df["Aging Status"] = np.select(conditions, choices)

# Merge the two df
df = df.merge(credit, on="Name")

#Sort and re-index df
df = df.sort_values(by=["Name", "Date"], ascending=True)
df = df.reset_index(drop=True)

#Calculate for FIFO balances
FIFO_balance = []
bal_bf = 0
indexor = -1
indexor2 = 0
dc_columns = list(df["Name"].unique())

for i in df["Amount"]:
   indexor += 1
   if df["Name"][indexor] == dc_columns[indexor2]:
      bal = min(i, df["Total Credit"][indexor] - bal_bf)
      FIFO_balance.append(bal)
      bal_bf += bal
   else:
      bal_bf = 0
      indexor2 += 1
      bal = min(i, df["Total Credit"][indexor] - bal_bf)
      FIFO_balance.append(bal)
      bal_bf += bal
      
df["Fifo Balance"] = FIFO_balance


# Calculate for actual balances
df["Actual Balance"] = df["Amount"] - df["Fifo Balance"]


# Summerize result
df_out = df.pivot_table(columns='Aging Status',
                  values='Actual Balance',
                  index='Name',
                  aggfunc='sum',
                  margins=True,
                  margins_name='Grand Total'
                  )