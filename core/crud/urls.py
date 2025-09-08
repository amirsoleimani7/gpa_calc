from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('' , views.main_page , name='main_page') ,
    path('update/<int:pk>/' , views.update_recipe , name='update_recipe') , 
    path('delete/<int:pk>/' , views.delete_recipe , name='delete_recipe') , 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)