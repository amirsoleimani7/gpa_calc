from django.urls import path , include
from . import views

urlpatterns = [
    
    path('' , views.index , name='index'),
    path('register/' , views.register_user , name='register'),
    path('activate/<str:uidb64>/<str:token>/' , views.activate , name='activate') , 
    path('accounts/' , include('django.contrib.auth.urls')), 
]