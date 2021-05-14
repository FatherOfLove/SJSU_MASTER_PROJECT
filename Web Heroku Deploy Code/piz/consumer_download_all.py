import pandas as pd  # 0.24.2
import numpy as np
from piz.models import Data_info
from piz.models import Result_info
from piz.models import Model_info
from django.contrib.auth.models import User
from piz import views
from django.http import HttpResponse


def download_all_as_csv(request):
    data_record_list = Data_info.objects.filter(user=User.objects.get(
        id=request.user.id))
    user_id = str(request.user.id)
    print(data_record_list)
    data_id_list = data_record_list.values('data_id')
    print("data_list", data_id_list)
    print("data_list type", type(data_id_list))
    result_id_list = data_record_list.values_list('result')
    print("result_list", result_id_list)
    access_code_list = []
    label_list = []
    for i in result_id_list:
        print(i)
        print(i[0])
        result_record = Result_info.objects.get(id=i[0])
        access_code_list.append(result_record.access_code)
        label_list.append(result_record.label)
    # result_list = Result_info.objects.filter(id=result_id_list)
    #  = result_list.values('access_code')
    # print('access code', access_code_list)
    #  = result_list.values('label')
    df = pd.DataFrame(data=data_id_list)
    #df['data_id'] = data_id_list
    df['access_code'] = access_code_list
    df['label'] = label_list
    print(df.head(5))
    path = '/Users/xianghuihuang/bitbucket/sjsu_release1_1/Code/Django_V1/chronus-project/download_csv/'
    # df.to_csv(path+user_id+'.csv')
    file_path = path+user_id+'.csv'
    # views.download(request, file_path)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=filename.csv'

    df.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False, decimal=",")
    return response
    # return views.consumer_data_collection(request)
