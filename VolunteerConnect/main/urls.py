from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import *


app_name = 'main'


urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('home/', home, name='home'),
    path('register/', views.register, name='register'),
    # Provjere
    path('event/', view_event, name='view_event'),

    # Generički pogledi ListView
    path('events/', EventListView.as_view(), name='event_list'),
    path('participations/', ParticipationListView.as_view(), name='participation_list'),
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('attachments/', AttachmentListView.as_view(), name='attachment_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    
    # Generički pogledi DetailView
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('participation/<int:pk>/', ParticipationDetailView.as_view(), name='participation_detail'),
    path('attachment/<int:pk>/', AttachmentDetailView.as_view(), name='attachment_detail'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
    # Event
    path('events/add/', EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    
    # Comments
    path('events/<int:event_pk>/comments/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    
    # Participation
    path('events/<int:event_pk>/participate/', ParticipationCreateView.as_view(), name='participate_in_event'),
    path('event/<int:pk>/withdraw/', withdraw_from_event, name='withdraw_from_event'),

    # Attachment
    path('events/<int:event_pk>/attachments/add/', AttachmentCreateView.as_view(), name='attachment_add'),

    # REST

    # Events
    path('api/events/', EventListCreateView.as_view(), name='event_list_create'),
    path('api/events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

    # Users
    path('api/users/', UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
    
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)