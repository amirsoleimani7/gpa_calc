from django.urls import path
from . import views

urlpatterns = [
    path('result/' ,views.result_page , name='result_page'),
    path('delete/<int:pk>/' , views.delete_subject , name='delete_subject'),
    path('update/<int:pk>/' , views.update_subject , name='update_subject'),
    path('main_page/' , views.main_page , name='main_page'),
    path('login/' , views.login_page , name='login') ,
    path('logout/' , views.custom_logout ,name='logout') , 
    path('register/' , views.register_page  , name='register') , 
    path('pdf_generation/' , views.generate_pdf , name='generation_pdf'), 

]