from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def store(request):
    context={}
    return render(request, 'store/store.html',context)

def home(request):
    return render(request, 'store/home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful account creation
    else:
        form = UserCreationForm()
    return render(request, 'store/account.html', {'form': form})

def size(request):
    context={}
    return render(request, 'store/size.html',context)

def chart(request):
    context={}
    return render(request, 'store/chart.html',context)

def figure(request):
    context={}
    return render(request, 'store/figure.html',context)


def logout(request):
    django_logout(request)
    return redirect('login')