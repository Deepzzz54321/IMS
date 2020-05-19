from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('home/', views.official_home, name='official_home'),
    path('maintainence', views.maintainence, name='maintainence'),
    path('unusable', views.unusable, name='unusable'),
    path('stock', views.stock, name='stock'),
    path('unmet-requirements', views.unmet_require, name='unmet_require'),
    path('products', views.products, name='products'),
    path('profile', views.profile, name='profile'),

    
]