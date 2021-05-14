from django.shortcuts import render
import numpy as np
import pandas as pd
from piz import models
from piz.models import Data_info
from piz.models import Result_info
from piz.models import Model_info
from piz import ECG_convertor
from piz import file_utils
from piz import db_operation_ORM
from piz import modeling
from piz import model_manage
from piz import visualize
from piz import data_management
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
import io
import os
from django.core.files import File
from django.conf import settings
from django.core.exceptions import ValidationError
import re
import datetime
from django.contrib.auth.models import User
from pathlib import Path
from django.contrib.auth import logout
BASE_DIR = Path(__file__).resolve().parent.parent


def download(request, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def logout_view(request):
    logout(request)
    return home(request)


def home(request):
    return render(request, 'piz/home.html')

# def home_tag(request,tag):
#     return render(request, 'piz/home.html'+tag)
# Create your views here.


def admin(request):
    context = db_operation_ORM.get_info_for_admin_dash(request)
    if 'error_info' in context:
        return render(request, 'piz/error.html', context)
    return render(request, 'piz/admin.html', context)


def clinicians(request):
    return render(request, 'piz/clinicians.html')


def clinicians_dashboard(request):
    context = db_operation_ORM.get_info_for_admin_dash(request)
    # print(context)
    if 'error_info' in context:
        return render(request, 'piz/error.html', context)
    return render(request, 'piz/clinicians_dashboard.html', context)


def consumer_result_view(request, result_id):
    context = {}
    result_record = Result_info.objects.get(id=int(result_id))
    data_record = Data_info.objects.get(result=result_record)
    context['data_id'] = data_record.data_id
    context['user_id'] = data_record.user.id
    context['label'] = result_record.label
    context['prob'] = result_record.prob
    context['result_id'] = result_record.result_id
    context['model_id'] = result_record.model_id
    context['prob'] = context['prob'] .split(',')
    context['access_code'] = result_record.access_code
    context['labels'] = ["Healthy", "Unhealthy"]
    context['data_path'] = str(settings.BASE_DIR) + data_record.data_path
    x = visualize.load_data(context['data_path'])
    context["chart1"] = visualize.get_signal_graph1(x)
    context["chart2"] = visualize.get_signal_graph2(x)
    context["chart3"] = visualize.get_signal_graph3(x)
    context["chart4"] = visualize.get_signal_graph4(x)
    context["chart5"] = visualize.get_signal_graph5(x)
    context["chart6"] = visualize.get_signal_graph6(x)
    context["chart7"] = visualize.get_signal_graph7(x)
    context["chart8"] = visualize.get_signal_graph8(x)
    context["chart9"] = visualize.get_signal_graph9(x)
    context["chart10"] = visualize.get_signal_graph10(x)
    context["chart11"] = visualize.get_signal_graph11(x)
    context["chart12"] = visualize.get_signal_graph12(x)
    # context["chart13"] = visualize.get_signal_graph13(x)
    # context["chart14"] = visualize.get_signal_graph14(x)
    # context["chart15"] = visualize.get_signal_graph15(x)
    return render(request, 'piz/consumer_result_view.html', context)


def user_result_view(request, result_id):
    context = {}
    result_record = Result_info.objects.get(id=int(result_id))
    print(result_record)
    data_record = Data_info.objects.get(result=result_record)
    print(data_record)
    context['data_id'] = data_record.data_id
    context['user_id'] = data_record.user.id
    context['data_path'] = data_record.data_path
    path = str(settings.BASE_DIR) + context['data_path']
    context["data_size"] = os.path.getsize(path)
    context['label'] = result_record.label
    context['prob'] = result_record.prob
    context['result_id'] = result_record.result_id
    context['model_id'] = result_record.model_id
    context['prob'] = context['prob'] .split(',')
    context['access_code'] = result_record.access_code
    context['labels'] = ['Healthy', 'Unhealthy']

    return render(request, 'piz/user_result_view.html', context)


def consumer(request):
    context = modeling.predict_by_data(request)
    if 'error_info' in context:
        return render(request, 'piz/error.html', context)
    return render(request, 'piz/consumer.html', context)


def consumer_data(request):
    result_list = []
    result_list = Data_info.objects.filter(
        user=request.user).values_list('result')
    for result in result_list:
        print(result)
        result = result.values_list()
        result_list.append(result)
    return render(request, 'piz/result_list.html', {'result_list': result_list})


def patient(request):
    context = visualize.get_pie_chart_by_access_code(request)
    if 'error_info' in context:
        return render(request, 'piz/error.html', context)
    data_path = str(settings.BASE_DIR) + \
        db_operation_ORM.get_datapath_with_access_code(request.POST['access_code'])
    print("data_path", data_path)
    x = visualize.load_data(data_path)

    print(x.shape)
    print(data_path)
    context["chart1"] = visualize.get_signal_graph1(x)
    context["chart2"] = visualize.get_signal_graph2(x)
    context["chart3"] = visualize.get_signal_graph3(x)
    context["chart4"] = visualize.get_signal_graph4(x)
    context["chart5"] = visualize.get_signal_graph5(x)
    context["chart6"] = visualize.get_signal_graph6(x)
    context["chart7"] = visualize.get_signal_graph7(x)
    context["chart8"] = visualize.get_signal_graph8(x)
    context["chart9"] = visualize.get_signal_graph9(x)
    context["chart10"] = visualize.get_signal_graph10(x)
    context["chart11"] = visualize.get_signal_graph11(x)
    context["chart12"] = visualize.get_signal_graph12(x)
    # context["chart13"] = visualize.get_signal_graph13(x)
    # context["chart14"] = visualize.get_signal_graph14(x)
    # context["chart15"] = visualize.get_signal_graph15(x)
    return render(request, 'piz/patient.html', context)


def signup(request):
    return render(request, 'piz/signup.html')


def contactus(request):
    return render(request, 'piz/contactus.html')


def access_code(request):
    logout(request)
    return render(request, 'piz/access_code.html')


def user_info_setting(request, user_id):
    context = {}
    context['user_data'] = User.objects.get(id=int(user_id))
    if request.method == "POST":
        # print(user_id)
        db_operation_ORM.edit_user_info(request, int(user_id))
        return clinicians_dashboard(request)
    return render(request, 'piz/user_info_setting.html', context)


def model_test(request):
    context = modeling.predict_by_data(request)
    if 'error_info' in context:
        return render(request, 'piz/error.html', context)
    # plot_pie_chart(context['predict'])
    return render(request, 'piz/model_test.html', context)


def user_management(request):
    context = {}
    context['user_data'] = User.objects.all().order_by("id")
    print(context['user_data'])
    return render(request, 'piz/user_management.html', context)


def model_management(request):
    context = model_manage.update_model(request)
    print(context.get('error_info', False))
    if context.get('error_info', False) is not False:
        return render(request, 'piz/error.html', context)
    # model_manage.update_model(request)
    #context = {}
    context['model_list'] = list(Model_info.objects.all().order_by('-model_id').values_list(
                                 'model_id', 'version', 'project_type', 'model_type', 'is_default'))

    return render(request, 'piz/model_management.html', context)

# def data_management(request):
#     return render(request, 'piz/model_management.html')


def data_collection(request):
    context = {}
    context['data_path'] = []
    context["data_list"] = Data_info.objects.all().values_list("data_path")
    context["all_data_list"] = Data_info.objects.all().order_by("data_id").values_list()
    for i in range(len(context["data_list"])):
        context["q_to_list"] = list(context["data_list"][i])
        a = [context["q_to_list"][0]]
        context['data_path'].append(a)
    return render(request, 'piz/data_collection.html', context)


def consumer_data_collection(request):
    context = {}
    context["consumer_data_list"] = Data_info.objects.order_by("data_id").filter(
        user_id=request.user.id).values_list()
    # data_management.get_only_user_data(user_id)
    return render(request, 'piz/consumer_data_collection.html', context)


def admin_view_consumer_data_collection(request, user_id):
    context = {}
    context["consumer_data_list"] = Data_info.objects.order_by("data_id").filter(
        user=User.objects.get(id=user_id)).values_list()
    # data_management.get_only_user_data(user_id)
    return render(request, 'piz/admin_view_consumer_data_collection.html', context)
