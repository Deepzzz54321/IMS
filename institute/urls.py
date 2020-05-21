from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('home/', views.official_home, name='official_home'),
    path('inventory-section-home', views.inven_home, name='inven_home'),
    path('inventory-requests', views.inven_requests, name='inven_requests'),
    path('maintainence', views.maintainence, name='maintainence'),
    path('unusable', views.unusable, name='unusable'),
    path('stock', views.stock, name='stock'),
    path('register-employee', views.register, name='register'),
    path('unmet-requirements', views.unmet_require, name='unmet_require'),
    path('products', views.products, name='products'),
    path('profile', views.profile, name='profile'),

    
]