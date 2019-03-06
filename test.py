# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html
import pandas as pd 

# with open('seed_data/scores.csv') as f:
#     data = f.read()

data = pd.read_csv('seed_data/scores.csv')

# data.groupby("performer_id").size()
# data.set_index("performer_id")
d = data.pivot(index='performer_id', columns='producer_id', values='score')

# print(d.head())
print(d)