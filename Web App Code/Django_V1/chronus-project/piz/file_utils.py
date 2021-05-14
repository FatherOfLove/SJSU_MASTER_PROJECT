import os
import pandas as pd
from piz import ECG_convertor
from django.conf import settings
from pathlib import Path
import numpy as np
import pywt

BASE_DIR = Path(__file__).resolve().parent.parent

symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']


def validate_data_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv', '.json']
    if not ext.lower() in valid_extensions:
        #raise ValidationError("error")
        return False


def validate_model_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.h5']
    if not ext.lower() in valid_extensions:
        #raise ValidationError("error")
        return False


def csv_json_validate_ECG_2020(path):
    if path.endswith('.json'):
        df = pd.read_json(str(BASE_DIR)+path).reset_index()
        df['sig_data'] = df.sig_data.apply(np.array)
        df_sig = df['sig_data']
        df_sig = denoise_all_ECG2020(df_sig)
        return df_sig
    else:
        df = pd.read_csv(str(BASE_DIR)+path).reset_index()
        df['sig_data'] = csv_data_to_int_new(df['sig_data'])
        df_sig = df['sig_data']
        df_sig = denoise_all_ECG2020(df_sig)
        return df_sig


def csv_json_validate(path):
    if path.endswith('.json'):
        print('enter function path:', str(BASE_DIR)+path)
        x = pd.read_json(str(BASE_DIR)+path)
        x = x.reset_index()
        x = read_data(symbol_names, x)
        x = denoise_all(x)
        return x
    else:
        x = pd.read_csv(str(BASE_DIR)+path)
        x = x.reset_index()
        x = csv_data_to_int(x)
        x = read_data(symbol_names, x)
        x = denoise_all(x)
        return x


def csv_data_to_int(data):
    for i in range(len(symbol_names)):
        a = symbol_names[i]
        x = data[a].to_list()
        x = ECG_convertor.Convert(x[0])
        x = x[0:30000]
        x = [float(i) for i in x]
        data[a][0] = x
    return data


def csv_data_to_int_new(data):
    data = ECG_convertor.Convert(data)
    data = [float(i) for i in x]
    data = np.array(data).reshape(12, 5000)
    return data


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


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


def read_data(symbol_names, data):
    for i in symbol_names:
        data[i] = data[i].apply(np.array)
    return data


def denoise_all(data):
    for i in symbol_names:
        for j in range(len(data)):
            data[i][j] = denoise(data[i][j])
    return data


def denoise_all_ECG2020(data):
    for i in range(len(data)):
        data[i] = denoise(data[i])
    return data
