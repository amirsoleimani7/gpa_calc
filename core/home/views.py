from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .models import Subject

def home(request):
    return HttpResponse("sup!")


def update_subject(request , pk):

    if request.method == 'POST':  
        try : 
            query_subject = Subject.objects.filter(pk=pk) # geting that object i guess              
            new_name = request.POST.get('new_name')
            new_grade= request.POST.get('new_grade')
            new_credits = request.POST.get('new_credits')
            if not query_subject.exists(): 
                messages.error(request, "the subject was not found !")     
                return redirect('update_subject')
            else: 
                print("the query ws found!")
                query_subject.name = new_name
                query_subject.grade = new_grade
                query_subject.credits = new_credits
                query_subject.save()
                messages.success(request,"the subject was updated")
                return redirect('update_subject')
        except Exception as e:
            print(f"the error is : {e}")
            print("some exception happened !")
   
    
    query_subject = Subject.objects.filter(pk=pk)[0] # geting that object i guess              
    
    print(f"the user {query_subject.user} , name is : {query_subject.name} , grade  : {query_subject.grade}")

    context = {
        'subject' : query_subject
    }

    return render(request , 'update_subject.html' , context)







@login_required(login_url='/accounts/login/')
def main_page(request):

    user = request.user
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            grade = request.POST.get("grade")
            credits = request.POST.get("credits")
            print(f"the user is : {user}")
            print(f"the name is : {name}")
            print(f"the grade is : {grade}")
            print(f"the credits is : {credits}")
            subject_obj = Subject(user=user,name=name,grade=grade , credits =credits) 
            subject_obj.save()
        except:
            messages.error(request , 'some error happend')
            return redirect('main_page')

    all_subjects = Subject.objects.filter(user=request.user)
    context = {
        'all_subjects' : all_subjects
    }
    return render(request,'main_page.html' , context)




def login_page(request):
    if request.method == 'POST':
        try: 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request , 'username not found')
                return redirect('lgoin')
            user_obj = authenticate(username=username , password=password)
            if user_obj :
                login(request , user_obj)
                return redirect('main_page')
            messages.error(request , "wrong password")
            return redirect('login')
        except Exception as e:
            messages.error(request , "something went wrong")
            print(f"the error is : {e}")
            return redirect("login")
    return render(request , "login.html")



def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request , 'username is taken')
                return redirect('register')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request , 'account created!')
            return redirect("login")
        except Exception as e:
            messages.error(request , "something went wrong")
            return redirect("register")
    return render(request , 'register.html')

def custom_logout(requets):
    logout(requets)
    return redirect('login')