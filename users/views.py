from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User

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

# Login view
def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        # Authenticate using either email or username
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            try:
                # Try authenticating with email if the username fails
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# Home view
def home(request):
    return render(request, 'home.html')
