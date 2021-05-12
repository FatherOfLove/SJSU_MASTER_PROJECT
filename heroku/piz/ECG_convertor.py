import numpy as np
import pandas as pd
import pywt
import os
import wfdb
import io
from django.core.files.storage import FileSystemStorage

symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']


def getUserData_Length(user_id):
    # check the how many data for one user
    num = len("SQL")
    return num+1

# Python code to convert string to list


def Convert(string):
    li = list(string.split(" "))
    return li


class ECG_data_convertor():
    # data_convertor
    symbol_names = ['i', 'ii', 'iii', 'avr', 'avl', 'avf',
                    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']

    def __init__(self, path):  # , user_id, data_id):
        self.path = path
        #self.user_id = user_id
        #self.data_id = data_id

    def json_convertor(self):
        json_file = pd.read_json(io.StringIO(self.path.read().decode('utf-8')))

        # TODO:if the file is zip

        print("【json】 successful!")
        return json_file

    def csv_convertor(self):

        # TODO:if the file is zip
        csv_file = pd.read_csv(io.StringIO(self.path.read().decode('utf-8')), delimiter=',')
        for i in symbol_names:
            for j in csv_file.index:
                csv_file[i][j] = Convert(csv_file[i][j])
        csv_file.index = list(csv_file.index)
        print("【csv】 successful!")
        return csv_file

    def dat_convertor(self, path):

        # TODO:if the file is zip

        path_names = os.listdir(path)

        records = []

        for patient_path in path_names:
            PATH = os.path.join(path, patient_path)  # path
            if not os.path.isfile(PATH):
                FILES = os.listdir(PATH)

                # check the file format must contain .hea .dat .xyz

                # if not catch error

                for file in FILES:
                    if '.hea' in file:
                        # print(file)
                        # data_files.append(file)
                        record_path = os.path.join(PATH, file.split('.')[0])
                        record = wfdb.rdrecord(record_path)
                        records.append(record)

        dat_file = pd.DataFrame(columns=['record_name', 'gender', 'age', 'label'])
        record_names = []
        genders = []
        ages = []
        labels = []
        arrays_sigs = []
        for record in records:
            # print(record.record_name)
            record_names.append(record.record_name)
            genders.append(record.comments[1].split(':')[1])
            ages.append(record.comments[0].split(':')[1])
            labels.append(record.comments[4].split(':')[1])
            arrays_sigs.append(record.p_signal.T)
        dat_file.record_name = record_names
        dat_file.gender = genders
        dat_file.age = ages
        dat_file.label = labels
        dat_file['arrays_all'] = arrays_sigs

        channel_names = records[0].sig_name
        for i in range(15):
            dat_file[channel_names[i]] = dat_file.arrays_all.apply(lambda x: x[i])

        dat_file.drop(['arrays_all'], axis=1, inplace=True)

        print("【dat】 successful!")
        return dat_file

    def load_data(self):
        # print(self.path)
        if self.path.name.endswith(".json"):
            data = self.json_convertor()
            # print('hello')
        elif self.path.name.endswith(".csv"):
            data = self.csv_convertor()
        else:
            data = self.dat_convertor(self.path)
        print("load successful!")
        return tf.convert_to_tensor(data)

    def preprocessing(self, samples_num=30200):
        data = self.load_data()
        # set the data into same size
        for i in symbol_names:
            for j in data.index:
                data[i][j] = data[i][j][0:samples_num]
        print("preprocessing successful!")
        return data

    def denoise(self, data):
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

    def format(self, samples_num=30200):
        list_data = self.preprocessing(samples_num)
        data = list_data[symbol_names]
        # convert to array and denoise
        for i in symbol_names:
            data[i] = data[i].apply(np.array)
            for j in data.index:
                data[i][j] = self.denoise(data[i][j])
        print("denoise pass!")
        print("format successful!\n")
        return data

    def DL_reshape(self, samples_num=30200):
        data = self.format(samples_num)
        temp = []
        for i in data.index:
            for k in range(30000):
                for name in symbol_names:
                    temp.append(data[name][i][k])
        new_data = np.array(temp).reshape(len(data), 30000, 15)
        print("DL_reshape successful!\n")
        return new_data
