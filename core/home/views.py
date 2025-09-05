from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

def home(request):
    return HttpResponse("sup!")

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username , password=password)
    
    if user is not None:
        login(request , user) # user's id saved to the session of the request        
        return redirect('home')
    else:
        return HttpResponse("wrong info")
    

class signup_view(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
