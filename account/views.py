from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .forms import RegisterForm, ProfileForm, UserForm, LoginForm
from .models import ProfileModel

@login_required
def home_view(request):
    context = {
        'title': "Home"
    }
    return render(request,'account/home.html')


@login_required
def profile(request):
    profile = ProfileModel.objects.get(user=request.user)

    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('account:profile')
        elif 'change_password' in request.POST:
            pass

    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'title': "Profile"
    }
    return render(request, 'account/profile.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('katalog:book-list')
    
    if request.method == 'POST':
        form_login = LoginForm(data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('katalog:book-list')
            else:
                form_login.add_error(None, "Invalid username or password")
    else:
        form_login = LoginForm()

    context = {
        'heading': 'Login',
        'form_login': form_login,
    }
    return render(request, 'account/login.html', context)

def register(request):
    if request.method == 'POST':
        form_register = RegisterForm(request.POST)
        if form_register.is_valid():
            user = form_register.save()
            auth_login(request, user)
            return redirect('account:home')
    else:
        form_register = RegisterForm()
    return render(request, 'account/register.html', {'form_register': form_register})



def logout(request):
    auth_logout(request)
    return redirect('account:login')

@login_required
def edit_profile(request):
    user = request.user
    profile, created = ProfileModel.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'title': "Edit Profile",
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/edit_profile.html', context)
