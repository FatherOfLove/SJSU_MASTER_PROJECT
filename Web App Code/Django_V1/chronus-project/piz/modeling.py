# -*- coding: utf-8 -*-

from django.conf import settings
import pickle
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from django.core.files.storage import FileSystemStorage
from piz.models import Data_info
from piz.models import Result_info
from piz.models import Model_info
from django.contrib.auth.models import User
from piz.file_utils import validate_data_file_extension
from piz import PTBXL_preprocess
from piz import db_operation_ORM
import enum
import random
import datetime
from django.http import HttpResponse

# Using enum class create enumerations
# class Data_type(enum.Enum):
#    ECG=0
#    BLOODCELL=1
#
# class ML_type(enum.Enum):
#   DL=0
#   ML=1

# def check_data(user_id,data_id):
#     data_id_list = db_operation_ORM.get_user_dataID_list(user_id)
#     if data_id in data_id_list:


def predict_by_data(request):
    # label_dict = {0: " Myocarditis", 1: " Healthy control", 2: " Dysrhythmia", 3: " Myocardial infarction", 4: " Valvular heart disease", 5: " Hypertrophy", 6: " Bundle branch block", 7: " Cardiomyopathy", 8: " n/a", 9: " Stable angina",
    #               10: " Palpitation", 11: " Heart failure (NYHA)", 12: " Unstable angina"}
    label_dict = {0: " Healthy", 1: " UnHealthy"}

    context = {}
    label = ''
    probs = ''
    if request.method == "POST":
        # file validate
        # print("file input:", request.FILES.get('document', True))
        if request.FILES.get('document', False) is False:
            context['error_info'] = 'Please submit file!'
            return context
        uploaded_file = request.FILES['document']
        print('file size:', uploaded_file.size)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        valid1 = validate_data_file_extension(uploaded_file)
        if valid1 is False:
            context['error_info'] = 'Error File Format！'
            return context

        user_id = str(request.user.id)
        data_id = user_id + '_' + request.POST['data_id']
        # data_id_list = db_operation_ORM.get_user_dataID_list(user_id)
        data_id_list_object = Data_info.objects.filter(user=User.objects.get(
            id=request.user.id))
        data_id_list = data_id_list_object.values_list('data_id', flat=True)
        print(data_id_list)
        #df = pd.DataFrame(data=data_id_list)
        if user_id + '_' + request.POST.get('data_id') in data_id_list:
            context['error_info'] = 'The data id you enter already exist!'
            return context
        # if Data_info.objects.filter(user=User.objects.get(
        #     id= user_id + '_' + request.POST.get('data_id'))).exists():
        #     context['error_info'] = 'Please enter Data ID!'
        #     return context

        if request.POST.get('data_id', False) is False or request.POST.get('data_id', False) == '':
            # print("input data test2222")
            context['error_info'] = 'Please enter Data ID!'
            return context
        try:
            test = PTBXL_preprocess.PTBXL_preprocess(
                str(settings.BASE_DIR) + context['url']).load_data()
            # a = test.DL_reshape(samples_num=5000)
            print('test :', test)

            project_type = request.POST['project_type']
            model_default_info = db_operation_ORM.get_default_model_info(project_type)
            model_id = model_default_info.model_id
            model_type = model_default_info.model_type
            model_file_path = model_default_info.model_path
            model = Modeling(project_type, model_type, model_file_path)
            probs = model.model_predict(test)
            # print(probs)
            print("prediction successfully!")
            result_prob = str(probs)
            result_prob = result_prob.replace('[', '').replace(
                ']', '').replace(' ', ',').replace(',,', ',')
            context['predict'] = result_prob
            print('prediction result: ', context['predict'])
            label = context['label'] = label_dict[np.argmax(probs)]
            context['prob'] = np.max(probs)

            # save result to database
            db_operation_ORM.insert_result_info(
                user_id, data_id, context['url'], model_id, label, result_prob, 'null')
            context['access_code'] = db_operation_ORM.get_access_code_by_dataID(data_id)
        except:
            context['error_info'] = 'Please enter Valid Json File! The Shape Should be (5000,12)!'
            return context
    return context


class Modeling():

    def __init__(self, project_type, model_type, model_file_path):
        self.data_type = project_type
        self.ML_type = model_type
        # print(self.data_type)
        # print(self.ML_type)
        self.MODEL_DIR = model_file_path  # get the pre-train model file path
        self.model = self.load_model_m()

    def load_model_m(self):
        """
        load model from the model file
        """

        print('model file path:', self.MODEL_DIR)
        if self.ML_type == 'DL':
            # loading DL model and return instance
            return load_model(self.MODEL_DIR)

        # read Machine Learning model from model_pickle file
        if ML_type == 'ML':
            with open(self.MODEL_DIR, 'rb') as f:
                return pickle.load(f)

    def model_predict(self, df):
        """
        to predict the result with the model
        input : formated data fit the model
        input type DataFrame
        """
        return self.model.predict(df)
