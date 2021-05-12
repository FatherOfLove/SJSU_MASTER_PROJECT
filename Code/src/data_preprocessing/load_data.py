# -*- coding: utf-8 -*-

!pip install wfdb

"""## Download data"""

from google.colab import drive
drive.mount('/content/gdrive')

#!wget -r -N -c -np https://physionet.org/files/ptbdb/1.0.0/ /content/gdrive/

!ls

# Commented out IPython magic to ensure Python compatibility.
# %cd gdrive/

!ls

!ls /content/gdrive/My\ Drive/physionet.org

import os

data_path='/content/gdrive/My Drive/physionet.org/files/ptbdb/1.0.0'

####################opening the head file######################
# HEADERFILE=''
# f=open(data_path+HEADERFILE,"r")
# z=f.readline().split()
# num_of_sig,s_freq=int(z[1]),int(z[2])     #% number of signals，sample rate of data

# dformat,gain,bitres,zerovalue,firstvalue=[],[],[],[],[]

# for i in range(num_of_sig):
#     z=f.readline().split()
#     dformat.append(int(z[1]))     #format
#     gain.append(int(z[2]))     #number of integers per mV
#     bitres.append(int(z[3]))     #bitresolution
#     zerovalue.append(int(z[4]))     #integer value of ECG zero point
#     firstvalue.append(int(z[5]))     #first integer value of signal (to test for errors)
# f.close()

# num_of_sig,s_freq,bitres

# dformat,gain,bitres,zerovalue,firstvalue

# dformat,gain,bitres,zerovalue,firstvalue

import numpy as np


"""# read all data to pd dataframe"""

import os
import wfdb
data_path='/content/gdrive/My Drive/physionet.org/files/ptbdb/1.0.0'

def read_data_files(data_path,label_list):
  path_names=os.listdir(data_path)
 # for name in path_names:
  #  if not os.path.isdir(name):
#      path_names.remove(name) 
  i=0
  records=[]      
             
  for patient_path in path_names:
      PATH=os.path.join(data_path,patient_path)   #path
      #if not os.path.isfile(PATH):
      FILES=os.listdir(PATH)
         #print(FILES) 
        # data_files=[]             
      for file in FILES:
        if '.hea' in file:
              #print(file)
              # data_files.append(file)
            
          record_path=os.path.join(PATH,file.split('.')[0])
          record=wfdb.rdrecord(record_path)
          
          label = record.comments[4].split(':')[1]

          if  label in label_list:
            print(label,file)  
            records.append(record)

  return records         

#all_records=read_data_files(data_path)
label_records = read_data_files(data_path,[' Myocardial infarction', ' Healthy control'])

len(label_records)

type(label_records[0])

print(type(label_records[0].p_signal))

print(label_records[0].p_signal.shape)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import json
from keras.utils import to_categorical
import tensorflow as tf
from sklearn.model_selection import train_test_split

#Model function
from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau
from keras.constraints import max_norm
from sklearn.model_selection import train_test_split
import pywt
import datetime

label_records[0].p_signal

#!pip install heartpy

#!pip install heartpy
import heartpy as hp
import pandas as pd
import matplotlib.pyplot as plt

data = hp.scale_data(label_records[0].p_signal.T[0])
data0 = label_records[0].p_signal.T[0]
data0.shape

# get the location of R wave
working_data, measures = hp.process(data, 1000.0)
hp.plotter(working_data, measures)

# get index of R waves
peaklists = working_data['peaklist']
# remove the first one and last one
peaklists = peaklists[1:-1]
print("index of R waves：", peaklists)

# get the wave

records_sliced = []
for i in peaklists: 
  tem_data = data0[i - 400:i + 600] 
  records_sliced.append(tem_data)

plt.plot(tem_records_sliced[0]) 
title = str(peaklists[0]) 
plt.title(title) 
plt.show()

"""# wave_slicing"""

!pip install heartpy
import heartpy as hp
import pandas as pd
import pywt
import matplotlib.pyplot as plt
convert_label = {' Myocardial infarction':0, ' Healthy control':1}

# denoise  function
def denoise(data):
    # wavedec
    coeffs = pywt.wavedec(data=data, wavelet='db5', level=9)
    cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs

    # threshold
    threshold = (np.median(np.abs(cD1)) / 0.6745) * (np.sqrt(2 * np.log(len(cD1))))
    cD1.fill(0)
    cD2.fill(0)
    for i in range(1, len(coeffs) - 2):
        coeffs[i] = pywt.threshold(coeffs[i], threshold)

    rdata = pywt.waverec(coeffs=coeffs, wavelet='db5')
    return rdata

def wave_slicing(sig_data, pre_num, after_num, fs, slices_num):
    data_length = slices_num *(pre_num + after_num)
    if sig_data.shape[0] < data_length :
      print('data is less than ', data_length )
      return np.array()
    sig_data = denoise(sig_data[0:data_length])
    #print('sig_data shape',sig_data.shape)
    #print(sig_data)
  

    data_scale = hp.scale_data(sig_data)
    record_sliced = []
    try:
      # get the location of R wave
      working_data, measures = hp.process(hrdata= data_scale,
                                            sample_rate = fs,
                                            bpmmin=5, bpmmax= 300)
      # get index of R waves
      peaklists = working_data['peaklist']
      # remove the first one and last one
      peaklists = peaklists[1:-1]
      print("index of R waves：", peaklists , '\n len(peaklists):', len(peaklists))

      # get the wave
      for i in peaklists[0:slices_num]:
        #print(i)
        tem_data = data_scale[i - pre_num: i + after_num]
        #print('sliced data shape', tem_data.shape)
        #print('tem_data type:', type(tem_data))
        record_sliced.append(tem_data)
        #print('append tem_data')

      #plot sample
      #plt.plot(record_sliced[-1])
      #title = str(peaklists[-1])
      #plt.title(title)
      #plt.show()

      record_sliced = np.array(record_sliced).T

      print('record_sliced shape:',record_sliced.shape)
    
    except Exception as e:
      print('error:', e)

    return record_sliced
  
def make_dataset_waves(records, pre_num, after_num, fs, slices_num):
  labels=[]
  arrays_sigs=[]
  for record in records:
    #print(record.record_name)
    label = record.comments[4].split(':')[1]
    label_num = convert_label.get(label)
    #print(label)
    #print(label_num)
    labels.append(label_num)
    record_sliced_list = []
    for sig_data in record.p_signal.T:
      record_sliced = wave_slicing(sig_data, pre_num, after_num, fs, slices_num)
      record_sliced_list.append(record_sliced)
    
  arrays_sigs.append(np.array(record_sliced_list))
  arrays_sigs = np.array(arrays_sigs)
  labels = to_categorical(labels,2)
  return arrays_sigs, labels

#test
record0_sliced = wave_slicing(label_records[0].p_signal.T[0], pre_num = 400, after_num = 600 , fs = 1000, slices_num = 30)


X,y = make_dataset_waves(label_records, pre_num = 400, after_num = 600 , fs = 1000, slices_num = 30)
X.shape

y.shape

X.shape

# make whole dataset
convert_label = {' Myocardial infarction':0, ' Healthy control':1}
def make_dataset2(records): 
  labels=[]
  arrays_sigs=[]
  for record in records:
    #print(record.record_name)
    label = record.comments[4].split(':')[1]
    label_num = convert_label.get(label)
    #print(label)
    #print(label_num)
    labels.append(label_num)
    arrays_sigs.append(record.p_signal[0:30000])
  arrays_sigs = np.array(arrays_sigs)
  labels = to_categorical(labels,2)
  return arrays_sigs, labels

X , y = make_dataset2(label_records)

X.shape

y.shape

#split the train, test data from x,y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)#try stratify
#split the valid data from train data
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1) # 0.25 x 0.8 = 0.2

def buildModel():

    newModel = tf.keras.models.Sequential([
                                           
        tf.keras.layers.InputLayer(input_shape=(30000,15)),

        tf.keras.layers.Conv1D(filters=4, kernel_size=21, strides=1, padding='SAME', activation='relu'),
       
        tf.keras.layers.AvgPool1D(pool_size=1, strides=4, padding='SAME'),
        
        tf.keras.layers.Conv1D(filters=16, kernel_size=23, strides=1, padding='SAME', activation='relu'),
        
        tf.keras.layers.AvgPool1D(pool_size=1, strides=4, padding='SAME'),
       
        tf.keras.layers.Conv1D(filters=32, kernel_size=25, strides=1, padding='SAME', activation='elu'),
       
        tf.keras.layers.AvgPool1D(pool_size=1, strides=8, padding='SAME'),
       
        tf.keras.layers.Conv1D(filters=64, kernel_size=27, strides=1, padding='SAME', activation='relu'),
       
        tf.keras.layers.Flatten(),
       
        tf.keras.layers.Dense(128, activation='relu'),
       
        tf.keras.layers.Dropout(rate=0.2),
       
        tf.keras.layers.Dense(2, activation='softmax')
    ])

    return newModel

model_test2 = buildModel()
model_test2.summary()

# Commented out IPython magic to ensure Python compatibility.

# %load_ext tensorboard
model_test2.compile(optimizer = RMSprop(lr=0.00001, rho=0.9, epsilon=1e-08, decay=0.0) , 
                loss = "categorical_crossentropy", metrics=["accuracy"])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model_test2.fit(X_train, y_train, epochs=40, batch_size=8)

X_train.shape

X_test.shape

model_test2.evaluate(x= X_test, y = y_test, batch_size = 1)


import pandas as pd
def make_dataset(records): 
  df = pd.DataFrame(columns = ['record_name','gender','age','label'])
  # array_0=records[0].p_signala
  # print(array_0)
  # plt.plot(array_0)
  record_names=[]
  genders=[]
  ages=[]
  labels=[]
  arrays_sigs=[]
  for record in records:
    #print(record.record_name)
    record_names.append(record.record_name) 
    genders.append(record.comments[1].split(':')[1]) 
    ages.append(record.comments[0].split(':')[1])  
    labels.append(record.comments[4].split(':')[1])
    arrays_sigs.append(record.p_signal.T)
  df.record_name=record_names
  df.gender=genders
  df.age=ages
  df.label=labels
  df['arrays_all']=arrays_sigs

  channel_names=records[0].sig_name
  for i in range(15):
    df[channel_names[i]]=df.arrays_all.apply(lambda x: x[i])
  
  df.drop(['arrays_all'],axis=1,inplace=True)
  return df

df=make_dataset(all_records)
df.shape

df.head(5)

