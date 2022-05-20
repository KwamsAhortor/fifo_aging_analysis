# Import modules
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

# Load data
xlsx = r"C:\Users\mfaraday01\Documents\Code\Aging Analysis\credit_debit_records.xlsx"
debit = pd.read_excel (xlsx, 
                     sheet_name="Debits"
                     )
credit = pd.read_excel (xlsx, 
                     sheet_name="Credit"
                     )

# Unipivot debit df
debit_unpiv = debit.melt(id_vars=["Zone", "Region", "District"], var_name="Date", value_name="Balance")

