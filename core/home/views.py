from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout

from django.contrib import messages



def home(request):
    return HttpResponse("sup!")


def login_page(request):
    if request.method == 'POST':
        try: 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request , 'username not found')
                return redirect('/accounts/login/')
            user_obj = authenticate(username=username , password=password)
            if user_obj :
                login(request , user_obj)
                return redirect('receipts')
            messages.error(request , "wrong password")
            return redirect('/accounts/login')
        except Exception as e:
            messages.error(request , "something went wrong")
            print(f"the error is : {e}")
            return redirect("/accounts/login/")
    return render(request , "login.html")



def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request , 'username is taken')
                return redirect('/accounts/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request , 'account created!')
            return redirect("/accounts/login/")
        except Exception as e:
            messages.error(request , "something went wrong")
            return redirect("/accounts/register/")
    return render(request , 'register.html')

def custom_logout(requets):
    logout(requets)
    return redirect('login')