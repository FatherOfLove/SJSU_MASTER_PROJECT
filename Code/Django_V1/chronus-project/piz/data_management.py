from piz import db_operation_ORM
from django.core.files.storage import FileSystemStorage
from piz.models import Model_info, Data_info
from django.conf import settings
from piz.file_utils import validate_model_file_extension
import io
import os
import re
import datetime
from piz import modeling
from django.shortcuts import render
from django.http import HttpResponse
from piz import views
import psycopg2


def get_only_user_data(user_id):
    pass


def del_data(request, data_id):
    Data_info.objects.filter(data_id=data_id).delete()
    return views.consumer_data_collection(request)
