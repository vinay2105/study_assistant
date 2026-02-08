from django.shortcuts import render, redirect
from .models import User, Profile
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import login, logout, authenticate 
import random
from .utils import send_otp_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            request.session['reg_email'] = form.cleaned_data['email']
            request.session['reg_password'] = form.cleaned_data['password']
            request.session['reg_username'] = form.cleaned_data['username']
            
            otp = random.randint(1000, 9999)
            request.session['reg_otp'] = otp 

            send_otp_email(form.cleaned_data['email'], otp) 
            
            return redirect('verify_otp')
        
        return render(request, 'authentication/register.html', {
            'form': form, 
            'error': form.errors
        })
    
    return render(request, 'authentication/register.html', {
        'form': RegistrationForm()
    })

def verify_otp_view(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('reg_otp')
        
        if user_otp == str(session_otp):

            email = request.session['reg_email']
            username = request.session['reg_username']
            password = request.session['reg_password']
            
            user = User(email=email, username=username)
            user.set_password(password)
            user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            del request.session['reg_email']
            del request.session['reg_password'] 
            del request.session['reg_username']
            del request.session['reg_otp']
            
            return redirect('complete_profile') 
            
        else:
            return render(request, 'authentication/verify_otp.html', {
                'error': 'Invalid OTP'
            })
    
    return render(request, 'authentication/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'authentication/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def welcome_view(request):
    return render(request, 'authentication/welcome.html')


@login_required
def home_view(request):
    has_api_key = bool(request.user.profile.api_key and request.user.profile.api_key.strip())

    return render(
        request,
        'authentication/home.html',
        {
            "has_api_key": has_api_key
        }
    )

@login_required
def complete_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
        
    else:
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
    return render(request, 'authentication/complete_profile.html', {
        'form': form
    })

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'authentication/profile.html', {
        'profile': profile
    })

from django.contrib import messages

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '')
        profile.date_of_birth = request.POST.get('date_of_birth') or None
        profile.api_key = request.POST.get('api_key', '')
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    return render(request, 'authentication/profile.html', {
        'profile': profile
    })
