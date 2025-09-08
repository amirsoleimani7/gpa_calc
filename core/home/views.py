from django.shortcuts import render , redirect , HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .models import Subject


from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter




GRADE_POINTS = {
    'A' : 9,
    'S' : 10,
    'B' : 8,
    'C' : 7,
    'D' : 6,
    'F' : 0,
}

def home(request):
    return HttpResponse("sup!")



def generate_pdf(request):

    buf = io.BytesIO()

    c = canvas.Canvas(buf , pagesize=letter ,bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch , inch)
    textob.setFont('Helvetica' ,14)

    query_user = request.user
    subjects_of_the_user = Subject.objects.filter(user=query_user)

    total_credits = 0
    total_grade = 0

    for subject in subjects_of_the_user:
        total_credits += subject.credits
        total_grade += GRADE_POINTS[subject.grade]


    lines = [
    ]

    for subject  in subjects_of_the_user : 
        lines.append(f"{subject.name} , {subject.grade} , {subject.credits}")
        
    lines.append(f"cgpa is : {total_grade / total_credits}")


    for line in lines:
        textob.textLine(line )

    c.drawText(textob)
    c.showPage()

    c.save()
    buf.seek(0)

    return FileResponse(buf , as_attachment=True , filename='cgpa_report.pdf')










@login_required(login_url='/accounts/login/')
def result_page(request):

    query_user = request.user
    subjects_of_the_user = Subject.objects.filter(user=query_user)

    total_credits = 0
    total_grade = 0

    for subject in subjects_of_the_user:
        total_credits += subject.credits
        total_grade += GRADE_POINTS[subject.grade]

    context = {
        'query_subjects' : subjects_of_the_user , 
        'cgpa' : total_grade / total_credits , 
    }
    
    return render(request , 'result_page.html' , context)


@login_required(login_url='/accounts/login/')
def update_subject(request , pk):

    if request.method == 'POST':  
        try : 
            query_subject = Subject.objects.filter(pk=pk)[0] # geting that object i guess              
            new_name = request.POST.get('new_name')
            new_grade= request.POST.get('new_grade')
            new_credits = request.POST.get('new_credits')
            print(f"new_name : {new_name}")
            print(f"new_grade : {new_grade}")
            print(f"new_credits : {new_credits}")

            if not query_subject: 
                messages.error(request, "the subject was not found !")     
                return redirect('update_subject' , pk=pk)
            else: 
                print("the query ws found!")
                query_subject.name = new_name
                query_subject.grade = new_grade
                query_subject.credits = new_credits
                query_subject.save()
                messages.success(request,"the subject was updated")
                return redirect('update_subject' , pk=pk)
        except Exception as e:
            print(f"the error is : {e}")
            print("some exception happened !")
            messages.error(request , 'some errors happend!')

    query_subject = Subject.objects.filter(pk=pk)[0] # geting that object i guess              
    print(f"the user {query_subject.user} , name is : {query_subject.name} , grade  : {query_subject.grade}")
    context = {
        'subject' : query_subject
    }

    return render(request , 'update_subject.html' , context)


@login_required(login_url='/accounts/login/')
def delete_subject(request , pk):
    query_object = get_object_or_404(Subject , pk=pk)
    try : 
        query_object.delete()
        return redirect('main_page')
    except Exception as e:
        messages.error(request , 'some exceptions happened !')
        return redirect('main_page')



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
            user_obj.save(commit=)
            messages.success(request , 'account created!')
            return redirect("login")
        except Exception as e:
            messages.error(request , "something went wrong")
            return redirect("register")
    return render(request , 'register.html')

def custom_logout(requets):
    logout(requets)
    return redirect('login')