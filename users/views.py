from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group    

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'user/login.html')

@login_required
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        print(role)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_user')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email=email,
            password=make_password(password),  # hash the password
            is_staff=(role == 'staff' or role == 'admin' or role == 'manager'),
            is_superuser=(role == 'admin'),
        )
        my_group = Group.objects.get(name=role) 
        my_group.user_set.add(user)

        messages.success(request, f"{role.title()} account created successfully.")
        return redirect('add_user')


    return render(request, 'user/add_user.html')


def logout(request):
    auth_logout(request)
    return redirect('login')
