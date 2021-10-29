# -*- coding: utf-8 -*-
"""Cavity_search.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gRK_R0OekYbtStsTp9yhI5BCmJhkbrh6
"""

from toolfunc import input_process,output_process,true_alt_info
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model


AMP = load_model('C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\directive\cavity_search\LSTM_AMP_2.h5')
PHA = load_model('C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\directive\cavity_search\LSTM_PHA_1.h5')
# files = '/content/gdrive/MyDrive/Colab Notebooks/test/CPW-5-8.csv'

#Generate input data(amp,pha), and comparison(to find the prediction frequency range)
amp , pha , comparison = input_process(files)      # comparison[no.][0] for freq start, end for comparison[no.][1]
comparison = np.array(comparison)

# prediction 
amp_pred = AMP.predict(amp)
pha_pred = PHA.predict(pha)
true ,alt = output_process(amp_pred,pha_pred,comparison)  
fig = pd.read_csv(files)
zone = true_alt_info(true,alt,fig)
print(zone)

