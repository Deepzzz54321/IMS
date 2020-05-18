from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('home/', views.official_home, name='official_home'),
    path('unmet-requirements', views.unmet_require, name='unmet_require')
]