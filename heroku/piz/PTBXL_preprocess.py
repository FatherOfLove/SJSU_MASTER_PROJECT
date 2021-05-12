# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt
import io
import json
import tensorflow as tf


class PTBXL_preprocess():

    def __init__(self, path):  # , user_id, data_id):
        self.path = path

    def denoise(self, sig_data):

        sig_length = len(sig_data)
        # print("pywt.waverec 1")
        coeffs = pywt.wavedec(data=sig_data, wavelet='db8', level=9)
        cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs
        threshold = (np.median(np.abs(cD1)) / 0.6745) * (np.sqrt(2 * np.log(len(cD1))))
        cD1.fill(0)
        cD2.fill(0)
        for i in range(1, len(coeffs) - 2):
            coeffs[i] = pywt.threshold(coeffs[i], threshold)
        # print("pywt.waverec 2")
        rdata = pywt.waverec(coeffs=coeffs, wavelet='db8')
        # print("denoise data:")
        sig_array2 = rdata
        zero_array = np.zeros(sig_length,)
        if max(sig_array2) != 0:
            # rdata = sig_array2[0:sig_length]
            for i in range(len(sig_array2)):
                # print("denoise loop")
                zero_array[i] = sig_array2[i]

            rdata = np.nan_to_num(zero_array)
        else:
            print("denoise zero error!")
            return sig_data

        #print("denoise return successful! ")
        return rdata

    def json_convertor(self):
        # print(self.path)
        df = pd.read_json(self.path)
        print("read JSON successfully!")
        # path = self.path.read().decode('utf-8')
        # print(path)
        # json_file = pd.read_json(path)
        # JSON preprocessing
        # print(type(df.data[0]))
        #print('df', df)
        df.data[0] = self.denoise_data(df.data[0])
        print("denoise return successfully! ")
        # print(df.data[0].shape)
        df = df.data.to_list()
        data = np.array(df)
        # denoise data
        # data = denoise()

        # TODO:if the file is zip
        #print('data shape', data.shape)
        # print(data[0][0])
        # self.plot_graph(data[0])
        return data

    def plot_graph(self, data):
        plt.plot(data)

    def load_data(self):
        # print(self.path)
        if self.path.endswith(".json"):
            data = self.json_convertor()
            # print('hello')
        elif self.path.name.endswith(".csv"):
            data = self.csv_convertor()
        else:
            data = self.dat_convertor(self.path)
        print("load data successfully!")
        # self.plot_graph(data.T[0])
        return tf.data.Dataset.from_tensor_slices(data).batch(1)

    def denoise_data(self, data):
        # print(data.shape)
        # if data.shape[0] == 12 and data.shape[1] == 5000
        try:
            data = np.array(data).reshape(12, 5000)
            # print(data)
            for i, sig_array in enumerate(data):
                # print(i)
                # print(sig_array.shape)
                sig_array2 = self.denoise(sig_array)
                # print(i+1)
                data[i] = sig_array2
            data2 = data
            #print("denoise data type:", type(data2))
            #print("denoise data shape:", data2.shape)
            return data2.T
#       TODO: if data_array.T.shape[0] != 5000 or data_array.T.shape[1] != 12:
        except:
            print('Denoise error!')
            return data.T


# check the shape of the data here

# PTBXL_preprocess("/Users/xianghuihuang/Desktop/HR03363_1.json").load_data()

# def csv_convertor(self):
#
#     # TODO:if the file is zip
#     csv_file = pd.read_csv(io.StringIO(self.path.read().decode('utf-8')), delimiter=',')
#     for i in symbol_names:
#         for j in csv_file.index:
#             csv_file[i][j] = Convert(csv_file[i][j])
#     csv_file.index = list(csv_file.index)
#     print("【csv】 successful!")
#     return csv_file
