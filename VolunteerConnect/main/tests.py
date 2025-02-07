from django.utils.timezone import make_aware
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *

# Create your tests here.


# Events -  prvjera ispravnosti kreiranja objave

User = get_user_model()

class EventModelTest(TestCase):
    def setUp(self):
        # Kreiraj testnog korisnika
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Kreiraj testni događaj s vremenskom zonom
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date=make_aware(datetime(2025, 2, 10, 10, 0, 0)),  # Dodano make_aware
            location='Test Location',
            organizer=self.user
        )
    
    def test_event_creation(self):
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.description, 'This is a test event')
        self.assertEqual(self.event.organizer, self.user)

    def test_event_string_representation(self):
        self.assertEqual(str(self.event), self.event.title)


# Home - provjera pristupa korisnicima

from django.test import Client
from django.urls import reverse

User = get_user_model()

class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # Kreiranje testnog korisnika
            username='testuser',
            password='testpassword'
        )
        self.client = Client()

    def test_home_view_logged_in(self): # Funkcija za testiranje pristupa home stranici
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')


# CustomUserCreationForm


from .forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase): 
    def test_valid_form(self): # Testiranje registracije novog korisnika sa točnim podacima
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '123456789',
            'address': 'Test Address',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self): # Testiranje registracije novog korisnika sa netočnim podacima
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '123456789',
            'address': 'Test Address',
            'password': 'testpassword',
            'password2': 'wrongpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
