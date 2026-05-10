from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm 
from core.models import AuditLog

# Create your views here.
def register_view(request):
    if request.user.is_authenticated: 
        return redirect('core:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        AuditLog.objects.create(user = user, action = 'CREATE', entity_type = 'User', entity_id = user.pk)
        messages.success(request, 'Account created! Please Log in')
        return redirect('accounts:login')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request): 
    if request.user.is_authenticated: 
        return redirect('core:dashboard')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user: 
            login(request, user)
            AuditLog.objects.create(user = user, action = 'LOGIN', entity_type = 'User', entity_id = user.pk)
            return redirect('core:dashboard')
        else: 
            error = 'Invalid email or password'
    return render(request, 'accounts/login.html', {'error': error})

@login_required
def logout_view(request): 
    AuditLog.objects.create(user = request.user, action = 'LOGOUT', entity_type = 'User', entity_id = request.user.pk)
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request): 
    profile_form = ProfileUpdateForm(instance = request.user)
    password_form = PasswordChangeForm(user = request.user)

    if request.method == 'POST': 
        if 'update_profile' in request.POST: 
            profile_form = ProfileUpdateForm(request.POST, instance = request.user)
            if profile_form.is_valid(): 
                profile_form.save()
                AuditLog.objects.create(user = request.user, action = 'UPDATE', entity_type = 'User',
                                        entity_id = request.user.pk)
                messages.success(request, 'Profile Updated Successfully!')
                return redirect('accounts:profile')
        
        elif 'change_password' in request.POST: 
            password_form = PasswordChangeForm(user = request.user, data = request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Password Changed Successfully!')
                return redirect('accounts:profile')
        
    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form, 
        'password_form' : password_form,
    })