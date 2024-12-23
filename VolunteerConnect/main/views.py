from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required


# Homepage

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {
        'user': request.user,  # Trenutno prijavljeni korisnik
    }
    return render(request, 'main/home.html', context)

# Funkcija za odjavu
def custom_logout(request):
    logout(request) 
    return redirect('http://127.0.0.1:8000/home/')

# Funkcija za odjavu sa događaja
def withdraw_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participation = Participation.objects.filter(event=event, participant=request.user).first()

    if participation:
        participation.delete()
        messages.success(request, 'Uspješno ste odustali od sudjelovanja u događaju.')
    else:
        messages.error(request, 'Niste prijavljeni na ovaj događaj.')

    return redirect('main:event_detail', pk=event.pk)



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
    
from django.contrib.auth.mixins import LoginRequiredMixin

class ParticipationListView(LoginRequiredMixin, ListView):
    model = Participation
    template_name = 'main/ListView/participation_list.html'
    context_object_name = 'participations'

    def get_queryset(self):
        queryset = Participation.objects.filter(participant=self.request.user)

        # Filtriranje po organizatoru
        organizer = self.request.GET.get('user')
        if organizer:
            queryset = queryset.filter(event__organizer__username__icontains=organizer)

        # Pretraživanje po naslovu događaja
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(event__title__icontains=query)

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
    
# Event

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Kreiranje događaja
from django.shortcuts import redirect
from django.forms import modelform_factory
from .forms import AttachmentFormSet
from .models import Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date', 'location']  # Polja za Event
    template_name = 'main/Event/event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attachment_formset'] = AttachmentFormSet(self.request.POST, self.request.FILES)
        else:
            context['attachment_formset'] = AttachmentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']
        form.instance.organizer = self.request.user
        if form.is_valid() and attachment_formset.is_valid():
            self.object = form.save()
            attachment_formset.instance = self.object
            attachment_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('main:event_list')  # Nakon uspješnog kreiranja, preusmjeri na popis događaja

# Popis događaja
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'main/Event/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.all()

        # Filtriranje po imenu organizatora
        organizer = self.request.GET.get('user')
        if organizer:
            queryset = queryset.filter(organizer__username__icontains=organizer)

        # Pretraživanje po naslovu događaja
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

# Detalji događaja
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'main/Event/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodavanje svih priloga povezanih s događajem u kontekst
        context['attachments'] = self.object.attachments.all()
        event = self.get_object()
        user = self.request.user
        
        if user.is_authenticated:
            context['is_participating'] = Participation.objects.filter(event=event, participant=user).exists()
        else:
            context['is_participating'] = False
            
        return context

# Uređivanje događaja
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date', 'location']
    template_name = 'main/Event/event_form.html'

    def test_func(self):
        return self.get_object().organizer == self.request.user

    def get_success_url(self):
        return reverse_lazy('main:event_detail', kwargs={'pk': self.object.pk})

# Brisanje događaja
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'main/Event/event_confirm_delete.html'

    def test_func(self):
        return self.get_object().organizer == self.request.user

    def get_success_url(self):
        return reverse_lazy('main:event_list')
    
    
# Comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'main/Comment/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.event = Event.objects.get(pk=self.kwargs['event_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:event_detail', kwargs={'pk': self.kwargs['event_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_pk'] = self.kwargs['event_pk']  # Dodaj event_pk u kontekst
        return context
    
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Provjeri je li trenutni korisnik autor komentara
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Uspješno ste obrisali svoj komentar.')
    else:
        messages.error(request, 'Niste ovlašteni obrisati ovaj komentar.')

    return redirect('main:event_detail', pk=comment.event.pk)


# Participation

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Event, Participation


class ParticipationCreateView(LoginRequiredMixin, CreateView):
    model = Participation
    fields = []
    template_name = 'main/Participation/participation_form.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        form.instance.participant = self.request.user
        form.instance.event = Event.objects.get(pk=self.kwargs['event_pk'])
    
        if Participation.objects.filter(event=event, participant=self.request.user).exists():
            messages.warning(self.request, 'Već ste prijavljeni na ovaj događaj.')
            return redirect('main:event_detail', pk=event.pk)

        messages.success(self.request, 'Uspješno ste se prijavili na događaj!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('main:event_detail', kwargs={'pk': self.object.event.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_pk'] = self.kwargs['event_pk']
        return context
    
# Attachment
class AttachmentCreateView(LoginRequiredMixin, CreateView):
    model = Attachment
    fields = ['file']
    template_name = 'main/Attachment/attachment_form.html'

    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs['event_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:event_detail', kwargs={'pk': self.kwargs['event_pk']})
