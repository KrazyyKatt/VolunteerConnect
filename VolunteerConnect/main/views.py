from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth import logout

def home(request):
    return render(request, 'main/home.html')


def custom_logout(request):
    logout(request)  # Django funkcija za odjavu
    return redirect('http://127.0.0.1:8000/home/')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_staff = False
            user.is_superuser = False


            user.set_password(form.cleaned_data['password'])
            user.save()
            # Automatski prijavi korisnika nakon registracije
            login(request, user)
            return redirect('http://127.0.0.1:8000/home/')  # Zamijenite 'home' s nazivom vaše početne stranice
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

