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


# Generički pogledi ListView
from django.views.generic import ListView
from .models import *

class EventListView(ListView):
    model = Event
    template_name = 'main/ListView/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q') 
        date_query = self.request.GET.get('date') 

        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) | models.Q(description__icontains=search_query)
            )
        if date_query:
            queryset = queryset.filter(date__date=date_query)

        return queryset
    
class ParticipationListView(ListView):
    model = Participation
    template_name = 'main/ListView/participation_list.html'
    context_object_name = 'participations'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.GET.get('user')
        
        if user:
            queryset = queryset.filter(participant__username=user)
        
        
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(event__title__icontains=search_query) | models.Q(participant__username__icontains=search_query)
            )

        return queryset


class CommentListView(ListView):
    model = Comment
    template_name = 'main/ListView/comment_list.html'
    context_object_name = 'comments'
        

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.GET.get('author')

        if author:
            queryset = queryset.filter(author__username__icontains=author)


        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(content__icontains=search_query) | models.Q(author__username__icontains=search_query)
            )

        return queryset


class AttachmentListView(ListView):
    model = Attachment
    template_name = 'main/ListView/attachment_list.html'
    context_object_name = 'attachments'

    def get_queryset(self):
        queryset = super().get_queryset()
        filename = self.request.GET.get('filename')

        if filename:
            queryset = queryset.filter(file__icontains=filename)
    
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(file__icontains=search_query) | models.Q(event__title__icontains=search_query)
            )

        return queryset
    

class UserListView(ListView):
    model = CustomUser
    template_name = 'main/ListView/user_list.html' 
    context_object_name = 'users' 

    def get_queryset(self):
        """
        Filtriranje korisnika prema GET parametrima (username, email, phone_number).
        """
        queryset = super().get_queryset()
        username = self.request.GET.get('username')
        email = self.request.GET.get('email') 
        phone = self.request.GET.get('phone')

        if username:
            queryset = queryset.filter(username__icontains=username)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if phone:
            queryset = queryset.filter(phone_number__icontains=phone)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(username__icontains=search_query) | models.Q(email__icontains=search_query)
            )

        return queryset

    
# Generički pogledi DetailView
from django.views.generic import DetailView
from .models import *

class EventDetailView(DetailView):
    model = Event
    template_name = 'main/DetailView/event_detail.html' 
    context_object_name = 'event' 

    def get_context_data(self, **kwargs):
        """
        Dodavanje relacija u kontekst predloška (npr. komentari, sudjelovanja, prilozi).
        """
        context = super().get_context_data(**kwargs)
        event = self.get_object() 

        # Dodavanje relacija
        context['comments'] = event.comments.all() 
        context['participants'] = event.participants.all() 
        context['attachments'] = event.attachments.all() 

        return context
    

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'main/DetailView/comment_detail.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        """
        Dodavanje relacija u kontekst predloška.
        """
        context = super().get_context_data(**kwargs)
        comment = self.get_object()

        # Dodavanje relacija
        context['event'] = comment.event  
        context['author'] = comment.author 

        return context
    
class ParticipationDetailView(DetailView):
    model = Participation
    template_name = 'main/DetailView/participation_detail.html'
    context_object_name = 'participation'

    def get_context_data(self, **kwargs):
        """
        Dodavanje relacija u kontekst predloška.
        """
        context = super().get_context_data(**kwargs)
        participation = self.get_object()

        # Dodavanje relacija
        context['event'] = participation.event  
        context['participant'] = participation.participant 

        return context
    
class AttachmentDetailView(DetailView):
    model = Attachment
    template_name = 'main/DetailView/attachment_detail.html'
    context_object_name = 'attachment'

    def get_context_data(self, **kwargs):
        """
        Dodavanje relacija u kontekst predloška.
        """
        context = super().get_context_data(**kwargs)
        attachment = self.get_object()

        # Dodavanje relacija
        context['event'] = attachment.event 

        return context
    
class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'main/DetailView/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Dodavanje relacija u kontekst predloška.
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Dodavanje relacija
        context['organized_events'] = user.event_set.all() 
        context['participations'] = user.participations.all() 

        return context