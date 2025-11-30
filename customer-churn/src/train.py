import numpy as np
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
data_path = base_dir/'data'/'Telco_customer_churn.xlsx'

df = pd.read_excel(data_path)

print(df.head())