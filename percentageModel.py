import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report 

data = pd.read_csv('delays.csv', index_col=0)
print(data.head())
print(data.groupby('Snow Day').count())
print(data.isnull().sum())

X = data.drop(columns=['Snow Day', 'Date'], axis = 1)
y = data['Snow Day']
#Check double quotes

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("X_train shape:",X_train.shape)
print("X_test shape:",X_test.shape)
print("y_train shape:",y_train.shape)
print("y_test shape:",y_test.shape)

clf = RandomForestClassifier()  
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)

print(classification_report(y_test, predictions))

probabilities = clf.predict_proba(X_test)


#Gets probabilities based off index
# print("Probability: ", probabilities[20])

for i in range(150):
    print(i, "Probability: ", probabilities[i])





