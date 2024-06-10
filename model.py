from matplotlib import pyplot as plt
import numpy as np
import pickle 
import pandas as pd
from clib import get_params, get_tavg

s, tmin, tmax = get_params()
tavg = get_tavg(pd.to_datetime('today').normalize())
print(s, tmin, tmax, tavg)

sc = pickle.load(open('inflated.pkl', 'rb'))
# predict_data = np.array([s[0], tmin[0], tmax[0], tavg])
predict_data = np.array([38.0,0.6,5.0,1.7])
predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))

dtc = pickle.load(open('inflated.sav', 'rb'))
print(dtc.predict_proba(predict_data))
print(dtc.predict(predict_data))