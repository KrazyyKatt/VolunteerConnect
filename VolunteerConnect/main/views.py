from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth import logout

def home(request):
    return render(request, 'main/home.html')

# Funkcija za odjavu
def custom_logout(request):
    logout(request) 
    return redirect('http://127.0.0.1:8000/home/')

# Funkcija za registraciju
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_staff = False
            user.is_superuser = False


            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            return redirect('http://127.0.0.1:8000/home/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

