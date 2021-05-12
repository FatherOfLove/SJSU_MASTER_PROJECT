import django
from django.contrib.auth.models import AbstractUser
from django.db import models
#！pip install django-safedelete #firstly if it didn't be install
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from django.contrib.auth.models import User
# Create your models here.

class User_info(SafeDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  
    company = models.CharField('Company', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)


class Model_info(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    model_id = models.TextField(max_length=50)
    version = models.TextField(max_length=50)
    project_type = models.TextField(max_length=50)
    model_type = models.TextField(max_length=50)
    model_path = models.TextField(max_length=256)
    is_default = models.BooleanField()
    
class Result_info(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    model = models.ForeignKey(Model_info, on_delete=models.CASCADE) 
    label = models.TextField(max_length=50)
    prob = models.TextField(max_length=512)
    graph_path = models.TextField(max_length=256)
    access_code = models.TextField(max_length=50)
    result_id = models.TextField(max_length=50)

class Data_info(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_id = models.TextField(max_length=50)
    data_path = models.TextField(max_length=256)
    result = models.OneToOneField(Result_info, on_delete=models.CASCADE)



