from piz import db_operation_ORM
from django.core.files.storage import FileSystemStorage
from piz.models import Model_info
from django.conf import settings
from piz.file_utils import validate_model_file_extension
import io
import os
import re
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from piz import views
import psycopg2
from piz import file_utils


def update_model(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES['model_file']
        # (upload_to='/model', storage=upload_storage)
        print('model file size:', uploaded_file.size)
        fs = FileSystemStorage(location=settings.MODEL_ROOT)
        name = fs.save(uploaded_file.name, uploaded_file)
        #print('test!!!!', name)
        context['url'] = str(settings.MODEL_ROOT) + '/' + name
        valid2 = validate_model_file_extension(uploaded_file)
        print("file validation:", valid2)
        if valid2 is False:
            context['error_info'] = 'Error Model File Format！'
            return context
        model_type = request.POST['model_type']
        project_type = request.POST['project_type']
        model_count = Model_info.objects.all().count()
        model_id = str(datetime.datetime.now())+'_'+model_type + '_'+str(model_count+1)
        version = str(datetime.datetime.now())+'_'+model_type + \
            '_' + project_type+'_'+str(model_count+1)
        model_path = context['url']
        db_operation_ORM.insert_model_info(
            model_id, version, project_type, model_path, model_type, True)
    return context


def del_model(request, model_id):
    if request.user.is_staff:
        project_type = Model_info.objects.get(model_id=model_id).project_type
        model_file_path = Model_info.objects.get(model_id=model_id).model_path
        Model_info.objects.filter(model_id=model_id).delete()
        print('Delete model record:', model_id)
        file_utils.delete_file(model_file_path)
        print('Delete model file:', model_file_path)
        default_model_num = Model_info.objects.filter(
            project_type=project_type, is_default=True).count()
        if default_model_num == 0:
            return after_delete_default_model(request, project_type)
    return views.model_management(request)


def after_delete_default_model(request, project_type):
    context = {}
    context['model_list'] = list(Model_info.objects.filter(project_type=project_type
                                                           ).order_by('-model_id').values_list('model_id',
                                                                                               'version', 'project_type', 'model_type', 'is_default'))
    context['project_type'] = project_type
    return render(request, 'piz/delete_default_model.html', context)


def set_model_default(request, model_id):
    if request.user.is_staff:
        try:
            project_type = Model_info.objects.get(model_id=model_id).project_type
            default_model_num = Model_info.objects.filter(
                project_type=project_type, is_default=True).count()
            print('default model_num of ', project_type, 'is', default_model_num)
            if default_model_num > 1:
                print('Error!Default model number of:', project_type, ' more than one!!')
                Model_info.objects.filter(project_type=project_type).update(is_default=False)
                print('Set other not default!')
            if default_model_num == 1:
                model_default = Model_info.objects.get(
                    project_type=project_type, is_default=True)
                model_default.is_default = False
                model_default.save()

            model_to_be_default = Model_info.objects.get(model_id=model_id)
            model_to_be_default.is_default = True
            model_to_be_default.save()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    else:
        return views.home(request)
    return views.model_management(request)
