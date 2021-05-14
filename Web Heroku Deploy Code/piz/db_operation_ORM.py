# -*- coding: utf-8 -*-


# !pip install psycopg2

import psycopg2
import datetime
from piz.models import Data_info
from piz.models import Result_info
from piz.models import Model_info
from piz.models import User_info
import random
from django.contrib.auth.models import User
from piz import views
from django.http import HttpResponse


def get_info_for_admin_dash(request):
    context = {}
    try:
        # all data collection
        context['total_data_number'] = Data_info.objects.all().count()
        context['total_models_number'] = Model_info.objects.all().count()
        context['total_users_number'] = User.objects.all().count()
        context['total_data_errors'] = 0
        context['total_access_code_generated'] = Result_info.objects.all().count()
        context['total_results_delivered'] = Result_info.objects.all().count()
        # only user data collection
        context['user_data_number'] = Data_info.objects.filter(
            user=request.user).count()
        context['user_access_code_generated'] = Data_info.objects.filter(
            user=request.user).count()
        context['user_results_delivered'] = Data_info.objects.filter(
            user=request.user).count()
        # print(context)
        return context
    except:
        context['error_info'] = 'Data base Error'
        print(context)
        return context


def edit_user_info(request, user_id):
    try:
        print('user_id:', type(user_id))
        if request.user.is_staff or request.user.id == user_id:
            print('starting edit user_info')
            # print(request.POST)
            user_record = User.objects.get(id=user_id)
            # print('user_record1:',user_record)
            user_record.first_name = request.POST["first_name"]
            #print('set f_n')
            # print('last:',request.POST["last_name"])
            user_record.last_name = request.POST["last_name"]
            #print('set l_n')
            user_record.email = request.POST["email"]
            #print('set mail')
            user_record.save()
            print('user_record update success!', user_record)
            try:
                user_info_record = User_info.objects.get(user=user_record)
                print('user_info record is: ', user_info_record)

            except User_info.DoesNotExist:
                print('not user_info now')
                user_info_record = User_info(user=user_record)
            user_info_record.company = request.POST["company"]
            user_info_record.telephone = request.POST["telephone"]
            user_info_record.mod_date = datetime.datetime.now()
            user_info_record.save()
            print('user_info_record update success!', user_info_record)
    except (Exception, psycopg2.DatabaseError) as error:
        print('update error!', error)


def edit_user_activation(request, user_id):
    if request.user.is_staff:
        try:
            user_record = User.objects.get(id=user_id)
            user_record.is_active = not user_record.is_active
            user_record.save()
            return views.user_management(request)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return views.user_management(request)
    else:
        return views.home(request)

# def result_id_get_result(request, result_id):
#     try:
#         user_record = Result_info.objects.get(id=result_id)
#         user_record.is_active = not user_record.is_active
#         user_record.save()
#         return views.user_management(request)
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#         return views.user_management(request)


def insert_data_info(user_id, data_id, data_path, result):
    try:
        data_record = Data_info(user=User.objects.get(id=user_id),
                                data_id=data_id,
                                data_path=data_path,
                                result=result)
        data_record.save()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_result_info(user_id, data_id, data_path, model_id, label, prob, graph_path):
    try:
        access_code = data_id + '_' + str(random.randint(0, 1000))
        result_id = 'result' + '_' + data_id
        result_record = Result_info(model=Model_info.objects.get(model_id=model_id),
                                    label=label,
                                    prob=prob,
                                    graph_path=graph_path,
                                    access_code=access_code,
                                    result_id=result_id)
        result_record.save()
        # update data_info table
        insert_data_info(user_id, data_id, data_path, result_record)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_model_info(model_id, version, project_type, model_path, model_type, is_default):
    try:
        this_default_model_num = Model_info.objects.filter(
            project_type=project_type, is_default=True).count()
        print('default model_num:', this_default_model_num)
        if is_default is True:
            Model_info.objects.filter(project_type=project_type).update(is_default=False)
            print('Set other not default!')
        model_record = Model_info(model_id=model_id,
                                  version=version,
                                  project_type=project_type,
                                  model_type=model_type,
                                  model_path=model_path,
                                  is_default=True)
        model_record.save()
        # this_model_num2 = Model_info.objects.filter(
        #            project_type=project_type, model_type=model_type, is_default=True).count()
        #print('this_model_num after update:',this_model_num2)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_default_model_info(project_type):
    model_default = Model_info.objects.get(project_type=project_type, is_default=True)
    return model_default


def get_user_dataID_list(user_id):
    # check the how many data for one user
    try:
        data_records = Data_info.objects.filter(user=User.objects.get(id=user_id))
        # for data_id in data_records:
        #     print(data_id)
        # return len(data_id_records) + 1
        return data_records

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_access_code_by_dataID(data_id):
    try:
        result_record = Data_info.objects.get(data_id=data_id).result
        access_code = result_record.access_code
        return access_code
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_result_with_code(access_code):
    try:
        result_records = Result_info.objects.get(access_code=access_code)
        return result_records

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_datapath_with_access_code(access_code):
    try:
        result_record = get_result_with_code(access_code)
        data_path = Data_info.objects.get(result=result_record).data_path
        return data_path
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
