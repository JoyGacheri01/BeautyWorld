from django.db import models
from django.shortcuts import render, redirect
# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        username = email.split('@')[0]  # Use part of the email as username
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

def login(request):  # Renamed to avoid conflict with the `login` import
    if request.method == 'POST':
        username = request.POST['username']  # Use username for authentication
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
