"""chronus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
from piz import views
from register import views as v
from piz import model_manage, data_management
from django.conf import settings
from django.conf.urls.static import static
from piz import db_operation_ORM
from piz import consumer_download_all
from piz import admin_download_all


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('home_tag/<tag>/', views.home_tag, name='home_tag'),
    path('admin-management-page', views.admin, name='admin'),
    path('consumer', views.consumer, name='consumer'),
    path('consumer_data', views.consumer_data, name='consumer_data'),
    path('clinicians_dashboard', views.clinicians_dashboard, name='clinicians_dashboard'),
    path('download_all_as_csv', consumer_download_all.download_all_as_csv, name='download_all_as_csv'),
    path('admin_download_all_as_csv', admin_download_all.download_all_as_csv,
         name='admin_download_all_as_csv'),
    path('patient', views.patient, name='patient'),
    path('signup', views.signup, name='signup'),
    path('model_test', views.model_test, name='model_test'),
    path('consumer_result_view/<result_id>/', views.consumer_result_view, name='consumer_result_view'),
    path('user_result_view/<result_id>/', views.user_result_view, name='user_result_view'),
    path('edit_user_activation/<user_id>/',
         db_operation_ORM.edit_user_activation, name='edit_user_activation'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('user_management', views.user_management, name='user_management'),
    path('user_info_setting/<user_id>/', views.user_info_setting, name='user_info_setting'),
    path('model_management', views.model_management, name='model_management'),
    path('data_collection', views.data_collection, name='data_collection'),
    path('consumer_data_collection',
         views.consumer_data_collection, name='consumer_data_collection'),
    path('admin_view_consumer_data_collection/<user_id>/',
         views.admin_view_consumer_data_collection, name='admin_view_consumer_data_collection'),
    path('access_code', views.access_code, name='access_code'),
    path('register/', v.register, name="register"),
    path('', include("django.contrib.auth.urls")),
    path('contactus', views.contactus, name='contactus'),
    path('clinicians', views.clinicians, name='clinicians'),
    path('del_model/<model_id>/',  model_manage.del_model, name='del_model'),
    path('del_data/<data_id>/',  data_management.del_data, name='del_data'),
    path('set_model_default/<model_id>/',  model_manage.set_model_default, name='set_model_default'),
    path('download/<file_path>/',  views.download, name='download'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MODEL_URL, model_root=settings.MODEL_ROOT)
