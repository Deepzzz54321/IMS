from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('home/', views.official_home, name='official_home'),
]