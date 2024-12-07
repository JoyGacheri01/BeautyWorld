from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Signup view
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = email.split('@')[0]  # Use email prefix as username
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect('home')
    
    return render(request, 'signup.html')


def user_login(request):
    logging.info('Received login request')
    
    if request.method == 'POST':
        logging.info('Request method is POST')
        
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        logging.info(f'Attempting to authenticate user: {username_or_email}')
        
        # Authenticate using either email or username
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            logging.warning(f'Authentication failed for username: {username_or_email}')
            try:
                # Try authenticating with email if the username fails
                user = User.objects.get(email=username_or_email)
                logging.info(f'Found user by email: {username_or_email}')
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                logging.error(f'User does not exist with email: {username_or_email}')
                user = None
        
        if user:
            logging.info(f'User authenticated successfully: {username_or_email}')
            auth_login(request, user)
            return redirect('home')
        else:
            logging.error('Invalid credentials provided')
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    logging.info('Request method is not POST, rendering login page')
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')
