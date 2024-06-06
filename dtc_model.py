from matplotlib import pyplot as plt
import numpy as np
import pickle 
import pandas as pd
from clib import get_params, get_tavg

s, tmin, tmax = get_params()
tavg = get_tavg(pd.to_datetime('today').normalize())
print(s, tmin, tmax, tavg)

sc = pickle.load(open('StandardScaler-distance.pkl', 'rb'))
# predict_data = np.array([s[0], tmin[0], tmax[0], tavg])
predict_data = np.array([250, -12, 1, -6])
predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))

dtc = pickle.load(open('lr_model-distance.sav', 'rb'))
print(dtc.predict_proba(predict_data))
print(dtc.predict(predict_data))