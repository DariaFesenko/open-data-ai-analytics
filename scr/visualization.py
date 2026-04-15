import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/Acer/Downloads/pmg_contracts_info.csv')
df.hist()
plt.show()