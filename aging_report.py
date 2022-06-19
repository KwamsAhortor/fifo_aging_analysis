# Import modules
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