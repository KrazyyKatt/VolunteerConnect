from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required

def home(request):
    return render(request, 'main/home.html')

# Funkcija za odjavu
def custom_logout(request):
    logout(request) 
    return redirect('http://127.0.0.1:8000/home/')



@permission_required('main.view_event', raise_exception=True)
def view_event(request):
    return render(request, 'main/event.html')



# Funkcija za registraciju
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Postavljanje dopuštenja
            user.is_staff = False
            user.is_superuser = False
            user.set_password(form.cleaned_data['password'])
            user.save()

            user.user_permissions.clear()
            user_group = Group.objects.get(name='Users')
            user.groups.add(user_group)

            permissions_to_assign = [
                # Event
                'main.add_event',
                'main.view_event',
                'main.register_event',  
                'main.comment_event',   

                # Participation
                'main.add_participation',  
                'main.view_participation',

                # Comment
                'main.add_comment',
                'main.view_comment',

                # Attachment 
                'main.add_attachment',
                'main.view_attachment',
            ]
            for permission_codename in permissions_to_assign:
                try:
                    app_label, codename = permission_codename.split('.')
                    permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    user.user_permissions.add(permission)
                except Permission.DoesNotExist:
                    pass 

            login(request, user)
            return redirect('http://127.0.0.1:8000/home/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




