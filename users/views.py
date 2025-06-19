from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.save()
            # guardar la fecha de nacimiento en un perfil
            auth_login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a TodoZapatillas.")
            return redirect('inicio') 
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form, 'title': 'Registro de Usuario'})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('inicio')  # Cambia 'inicio' por la vista principal de tu proyecto
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


