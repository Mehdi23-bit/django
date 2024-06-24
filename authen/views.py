from django.shortcuts import render,redirect
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import LoginForm,SignInForm
from django.contrib import messages
def custom_logout_view(request):
    logout(request)  # Log out the user
    return redirect('login_page')  # Redirect to the login page


def validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(f"{value} is not a valid email address")



@login_required
def success(request):
    return render(request, 'success.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/success/')
    form = LoginForm()
    return render(request,'login.html',{'form':form})

def login_(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/success/')
            else:
                error_message = "Le nom d'utilisateur ou le mot de passe est incorrect."
                context = {'error_message': error_message,'form':form}
                return render(request, 'login.html', context)
            

    else:
        error_message = "vous avez des error en les information que vous submiter"
        context = {'error_message': error_message,'form':form}
        return render(request, 'login.html', context)
            
def sign_in(request):
    if request.method == 'POST':
        form=SignInForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request,"Vous enrigestrer l'utilisateur " +username+' avec succès' )
            return redirect('/login_page/')
            
        else:
           return render(request,'sign_in.html',{'form': form})
        
def sign_page(request):
   form=SignInForm()
   return render(request,'sign_in.html',{'form': form})