from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def str(self):
        return self.username
    
is_staff = models.BooleanField(default=False)
is_superuser = models.BooleanField(default=False)
    
# Objava događaja od strane korisnika
User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=200)  # Naslov događaja
    description = models.TextField()  # Opis događaja
    date = models.DateTimeField()  # Datum i vrijeme događaja
    location = models.CharField(max_length=255)  # Lokacija događaja
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)  # Organizator događaja
    created_at = models.DateTimeField(auto_now_add=True)  # Datum kreiranja objave
    updated_at = models.DateTimeField(auto_now=True)  # Datum zadnjeg ažuriranja

    def __str__(self):
        return self.title

# Komentiranje na događaje
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')  # Na koji događaj se komentar odnosi
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor komentara
    content = models.TextField()  # Sadržaj komentara
    created_at = models.DateTimeField(auto_now_add=True)  # Vrijeme objavljivanja komentara

    def __str__(self):
        return f"Comment by {self.author} on {self.event}"

# Prijava na događaje
class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')  # Na koji događaj se prijava odnosi
    participant = models.ForeignKey(User, on_delete=models.CASCADE)  # Korisnik koji se prijavio
    date_joined = models.DateTimeField(auto_now_add=True)  # Vrijeme kada je korisnik prijavljen

    def __str__(self):
        return f"{self.participant} participating in {self.event}"

# Dodavanje slika ili dokumenta na događaje
class Attachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')  # Povezano s događajem
    file = models.FileField(upload_to='attachments/')  # Datoteka (slika, dokument, itd.)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Vrijeme uploada

    def __str__(self):
        return f"Attachment for {self.event}"
