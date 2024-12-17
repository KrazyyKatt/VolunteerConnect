from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import *

app_name = 'main'


urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),
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
]
