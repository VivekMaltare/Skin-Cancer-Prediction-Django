#from typing import ContextManager
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

from django.core.mail import send_mail

import logging

try:
    # Get the logger named 'django'
    logger = logging.getLogger('django')
    print("Logger loaded successfully")
except Exception as e:
    print(f"Error loading logger: {e}")

# Create your views here.
def login(request):
    logger.info("Login Request")
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass2']
        
        user = auth.authenticate(username = email,password = password)
        if user is not None:
            logger.info("login successful")
            auth.login(request,user)
            return redirect('/')
        else:
            logger.info("invalid credentials")
            messages.info(request,'Invalid Credentials *_*')
            return render(request,'account/login,register.html')
    else:
        return render(request,'account/login,register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    logger.info("Register Request")
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        if User.objects.filter(username = username).exists():
            logger.info("email already exists")
            messages.info(request,'An Account with this email already exist *_*')
            return render(request,'account/login,register.html')
        if len(username)==0:
            logger.info("email not entered")
            messages.info(request,'Email-address not entered *_*')
            return render(request,'account/login,register.html')
        
        email = request.POST['email']
        password = request.POST['pass2']
        
        # user.profile.gender = getGender(request.POST['gender'])
        
        #fi = int(request.POST['phnum'])

        user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)

        user.save()
        # send_mail(
        #     'Welcome to Navkaar medical!!!',
        #     'Thanks for signing-up. Your are awsome!!!!!!',
        #     'Navkaarmedical@gmail.com',
        #     [email],
        #     fail_silently=False,
        # )

        logger.info("registration successful")
        return render(request,'account/login,register.html')
    else:
        return render(request,'account/login,register.html')