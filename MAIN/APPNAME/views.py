
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password
from .decorators import unauthenticated_user
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, 'Account was created for ' + username)

            return redirect('/')
        

    context = {'form':form}
    return render(request, 'register.html', context)

def home(request):
    if request.method == "POST":
        if "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "home.html", {
                    "code":code, 
                    "user":new_login,
                })

        elif "confirm" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                messages.error(request, msg)
                # return HttpResponseRedirect(request.path)
                context = {}
                return render(request, 'home.html', context)
            else:
                login(request, User.objects.get(username=user))
                msg = f"{request.user} welcome again."
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #ecrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            #get title of the website
            br.open(url)
            title = br.title()
            #get the logo's URL
            icon = favicon.get(url)[0].url
            #Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
            
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }   



    return render(request, "home.html", context)