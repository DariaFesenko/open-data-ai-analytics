import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/dataset.csv')
df.hist()
plt.show()