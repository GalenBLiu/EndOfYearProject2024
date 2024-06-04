from matplotlib import pyplot as plt
import numpy as np
import pickle 
import pandas as pd

dtc = pickle.load(open('dtc_model.sav', 'rb'))
sc = pickle.load(open('StandardScaler.pkl', 'rb'))
predict_data = np.array([50, -0.7, 11, 3])
predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))
print(dtc.predict(predict_data))