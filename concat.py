import pandas as pd

df1 = pd.read_csv('2018-01-01-2018-12-31.csv', index_col=0)
df2 = pd.read_csv('2019-01-01-2019-12-31.csv', index_col=0)
df3 = pd.read_csv('2020-01-01-2020-03-10.csv', index_col=0)
df4 = pd.read_csv('2021-06-30-2021-12-31.csv', index_col=0)
df5 = pd.read_csv('2022-01-01-2022-12-31.csv', index_col=0)
df6 = pd.read_csv('2023-01-01-2023-12-31.csv', index_col=0)
df7 = pd.read_csv('2024-01-01-2024-06-03.csv', index_col=0)

df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
print(df)
df.to_csv('2018-01-01-2024-05-27.csv')
