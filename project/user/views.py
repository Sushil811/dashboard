from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile_picture = request.FILES['profile_picture']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address_line1 = request.POST['address_line1']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        user_type = request.POST['user_type']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.profile.profile_picture = profile_picture
        user.profile.address_line1 = address_line1
        user.profile.city = city
        user.profile.state = state
        user.profile.pincode = pincode
        user.profile.user_type = user_type
        user.save()
        
        return redirect('login')
    
    return render(request, 'user/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request, 'user/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    return render(request, 'user/dashboard.html', {'user': user})
