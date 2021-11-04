from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import *
from store.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'userL': request.user.is_authenticated})
    else:
        return render(request, 'user/register.html')


def signOut(request):
    logout(request)
    return redirect('/home/')


def register(request):

    if request.method == "POST":
        first_name= request.POST['fname']
        last_name = request.POST['lname']
        mobNo     = request.POST['phonenumber']
        password1 = request.POST['passw']
        password2 = request.POST['cnf_passw']
        email     = request.POST['username']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                print("Email Taken")
                return render(request, 'login.html')

            else:
                user = User.objects.create_user(username=email, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                mobile=Userprofile(user_id=user.id,mobile=mobNo)
                mobile.save()

                userwa=User.objects.get(id=user.id)
                wallet=Wallet.objects.create(user=userwa)
                wallet.save()
                return render(request,'login.html')

        else:
            messages.info(request, "Enter correct password")
            return render(request, 'login.html')

    else:
        return render(request, 'index-12.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['passw']

        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            # messages.info(request, 'Success')
            return redirect('/home/')
        else:
            print('else ka')
            messages.info(request,'Check your Credentials...')
            return redirect('login')
    else:
        return render(request, 'login.html')