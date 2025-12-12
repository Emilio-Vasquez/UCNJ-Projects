import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys, os




## All dataframes are stored in the LIST "dfs" dfs[0] = bronx_df
def LOAD_DATA(DATA_DIR):
    boroughs = ["bronx", "brooklyn", "manhat", "queens", "staten"]
 

    dfs = []
    for i in boroughs:
        path = os.path.join(DATA_DIR,f"{i}_2021.xlsx")    
        df = pd.read_excel(path, skiprows=4)
        dfs.append(df)
    print("DATA LOADED :)")
    return dfs
    ##def Linear_Reg():



