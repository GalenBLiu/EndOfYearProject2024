from matplotlib import pyplot as plt
import numpy as np
import pickle 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier

data = pd.read_csv('InflatedSnow.csv', index_col=0)
print(data.head())
print(data.groupby('Snow Day').count())
print(data.isnull().sum())

X = data.drop(['Snow Day', 'Date'], axis=1)
y = data['Snow Day']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=True)
www = (X_train.iloc[0].to_numpy())
# y_train = y_train.values.reshape(-1,1)
# y_test = y_test.values.reshape(-1,1)
 
print("X_train shape:",X_train.shape)
print("X_test shape:",X_test.shape)
print("y_train shape:",y_train.shape)
print("y_test shape:",y_test.shape)

result_dict_train = {}
result_dict_test = {}

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# pickle.dump(sc, open('inflated.pkl', 'wb'))

reg = LogisticRegression(random_state = 42)
accuracies = cross_val_score(reg, X_train, y_train, cv=5)
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
 
print(y_test.to_numpy())
print(y_pred)

print("LR Train Score:",np.mean(accuracies))
print("Test Score:",reg.score(X_test,y_test))

result_dict_train["Logistic Train Score"] = np.mean(accuracies)
result_dict_test["Logistic Test Score"] = reg.score(X_test,y_test)

# filename = 'inflated.sav'
# pickle.dump(reg, open(filename, 'wb'))

xgb = XGBClassifier()
accuracies = cross_val_score(xgb, X_train, y_train, cv=5)
xgb.fit(X_train,y_train)
y_pred = xgb.predict(X_test)
 
print(y_test.to_numpy())
print(y_pred)

print("XGB Train Score:",np.mean(accuracies))
print("Test Score:",reg.score(X_test,y_test))

result_dict_train["XGB Train Score"] = np.mean(accuracies)
result_dict_test["XGB Test Score"] = reg.score(X_test,y_test)

dtc = DecisionTreeClassifier(random_state = 42)
accuracies = cross_val_score(dtc, X_train, y_train, cv=5)
dtc.fit(X_train,y_train)
y_pred = dtc.predict(X_test)

print(y_test.to_numpy())
print(y_pred)

print("DTC Train Score:",np.mean(accuracies))
print("Test Score:",dtc.score(X_test,y_test))

# filename = 'dtc_model.sav'
# pickle.dump(dtc, open(filename, 'wb'))

result_dict_train["Decision Tree Train Score"] = np.mean(accuracies)
result_dict_test["Decision Tree Test Score"] = dtc.score(X_test,y_test)

rfc = RandomForestClassifier(random_state = 42)
accuracies = cross_val_score(rfc, X_train, y_train, cv=5)
rfc.fit(X_train,y_train)
y_pred = rfc.predict(X_test)

print(y_test.to_numpy())
print(y_pred)

print("RFC Train Score:",np.mean(accuracies))
print("Test Score:",rfc.score(X_test,y_test))

result_dict_train["Random Forest Train Score"] = np.mean(accuracies)
result_dict_test["Random Forest Test Score"] = rfc.score(X_test,y_test)

# filename = 'rfc_model.sav'
# pickle.dump(rfc, open(filename, 'wb'))

df_result_train = pd.DataFrame.from_dict(result_dict_train,orient = "index",columns=["Score"])
df_result_test = pd.DataFrame.from_dict(result_dict_test,orient = "index",columns=["Score"])


import seaborn as sns

fig,ax = plt.subplots(1,2,figsize=(20,4))
fig.subplots_adjust(wspace=1)
sns.barplot(x = df_result_train.index,y = df_result_train.Score,ax = ax[0])
sns.barplot(x = df_result_test.index,y = df_result_test.Score,ax = ax[1])
ax[0].set_xticklabels(df_result_train.index,rotation = 30)
ax[0].set_ylim(0.90, 1)
ax[1].set_ylim(0.90, 1)
ax[1].set_xticklabels(df_result_test.index,rotation = 30)
fig.tight_layout()
plt.show()

predict_data = np.array([200, -12, -1, -8]).reshape(1,-1)
predict_data = sc.transform(predict_data)
currModel = reg #Model switcher
print(currModel.predict_proba(predict_data))
print(currModel.predict(predict_data))

