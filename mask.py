import pandas as pd

maskee = '2018-01-01-2024-06-03-distance'
mask = 'master_set_holidays.csv'
distance = pd.read_csv(maskee+'.csv', index_col=0)
master = pd.read_csv(mask, index_col=0)

print(len(master))
print(len(distance))
in_dist = 0
l = []

for i in range(len(master)):
    date = distance.iloc[in_dist].loc['Date']
    if date != master.iloc[i].loc['Date']:
        print('MASTER:', master.iloc[i].loc['Date'])
        while date != master.iloc[i].loc['Date']:
            print('\tDIST:', date)
            in_dist += 1
            date = distance.iloc[in_dist].loc['Date']
    l.append(distance.iloc[in_dist])
    in_dist += 1

print(len(l))
print(l)

df = pd.DataFrame(l)
print(df.head())
df.to_csv(f'{maskee}-holidays.csv')
