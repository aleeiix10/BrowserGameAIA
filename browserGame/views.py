from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

def index(request):
    context = {}

    return render(request, 'browserGame/index.html', context)

def pagina_inicio(request):
    if request.user.is_authenticated:
        return render(request, 'browserGame/index_protected.html')
    else:
        return render(request, 'browserGame/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})