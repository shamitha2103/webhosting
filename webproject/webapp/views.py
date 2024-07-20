from django.shortcuts import render,redirect
from django.contrib import messages

from webproject import settings
from.forms import RegisterForm, LoginForm, UpdateForm,ChangepasswordForm
from .models import Register,Gallery
from django.contrib.auth import logout as logouts
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request,'index.html')
def registration(request):
    if request.method=='POST':
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data['Name']
            age=form.cleaned_data['Age']
            photo=request.FILES['Photo']
            place=form.cleaned_data['Place']
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            user=Register.objects.filter(Email=email).exists()
            if user:
                messages.warning(request,'Email Alredy exist')
                return redirect('/login')
            elif password!=confirmpassword:
                messages.warning(request,'Password Mismatch')
            else:
                tab=Register(Name=name,Age=age,Place=place,Email=email,Photo=photo,Password=password)
                tab.save()
                subject='welcome to mysite'
                message=f'Hi{name},thank you for registering in ddddd'
                email_form=settings.EMAIL_HOST_USER
                receipient_list=[email,]
                send_mail(subject,message,email_form,receipient_list)
                messages.success(request,'DATA SAVED')
                return redirect('/')
    else:
        form=RegisterForm() 
    return render(request,'registration.html',{'form':form})
    
def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            try:
                user=Register.objects.get(Email=email)
                if not user:
                    messages.warning(request,'Email does not exist')
                    return redirect('/login')
                elif password!=user.Password:
                    messages.warning(request,'Password Incorrect')
                    return redirect('/login')
                else:
                    messages.success(request,'Success')
                    return redirect('/home/%s' % user.id)
            except:
                messages.warning(request,'Email or Password incorrect')
                return redirect('/login')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})
def home(request,id):
        user=Register.objects.get(id=id)
        return render(request,'home.html',{'user':user})

def update(request,id):
    user=Register.objects.get(id=id)
    if request.method=='POST':
        form=UpdateForm(request.POST or None,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Success')
            return redirect('/home/%s' % user.id)
    else:
        form=UpdateForm(instance=user)
    return render(request,'update.html',{'user':user,'form':form})

def delete(request):
    user=Register.objects.get(id=id)
    user.delete()
    messages.success(request,'SUCCESS')
    return redirect('/')

def logout(request):
    logouts(request)
    messages.success(request,'SUCCESS')
    return redirect('/')

def changepassword(request,id):
    user=Register.objects.get(id=id)
    if request.method=='POST':
        form=ChangepasswordForm(request.POST or None)
        if form.is_valid():
            oldpassword=form.cleaned_data['OldPassword']
            newpassword=form.cleaned_data['NewPassword']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            if oldpassword!= user.Password:
                messages.warning(request,"incorrect")
                return redirect('/changepassword/%s' % user.id)
            elif oldpassword==newpassword: 
                messages.warning(request, "password similar")
                return redirect('/changepassword/%s' % user.id)
            elif newpassword!=confirmpassword:
                messages.warning(request,"password new")
                return redirect('/changepassword/%s'% user.id)
            else:
                user.Password=newpassword
                user.save()
                messages.success(request,"change success")
    else:
        form=ChangepasswordForm()
        return render(request,'changepassword.html',{'user':user, 'form':form})

def logout(request):
    logouts(request)
    messages.success(request,"logged out")
    return redirect('/')

def gallery(request):
    images=Gallery.objects.all()
    return render(request,'gallery.html',{'images':images})

def details(request, id): 
    images=Gallery.objects.get(id=id)
    return render(request,'details.html',{'images':images}) 
