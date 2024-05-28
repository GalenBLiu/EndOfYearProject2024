import pandas as pd

df1 = pd.read_csv('2022-01-01-2022-12-31.csv', index_col=0)
df2 = pd.read_csv('2023-01-01-2023-12-31.csv', index_col=0)
df3 = pd.read_csv('2024-01-01-2024-05-27.csv', index_col=0)

df = pd.concat([df1, df2, df3], ignore_index=True)
print(df)
df.to_csv('2022-01-01-2024-05-27.csv')
