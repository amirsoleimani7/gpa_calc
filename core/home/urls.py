from django.urls import path
from . import views

urlpatterns = [
    path('main_page/' , views.main_page , name='main_page'),
    path('login/' , views.login_page , name='login') ,
    path('logout/' , views.custom_logout ,name='logout') , 
    path('register/' , views.register_page  , name='register')
]