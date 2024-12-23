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
    title = models.CharField(max_length=200) 
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Dopuštenja
    class Meta:
        default_permissions = ()
        permissions = [
            ("add_event", "Can add event"),
            ("view_event", "Can view event"),
            ("register_event", "Can register for event"),
            ("comment_event", "Can comment on event"),
        ]

    def __str__(self):
        return self.title

# Komentiranje na događaje
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        permissions = [
            ("add_comment", "Can add comment"),
            ("view_comment", "Can view comment"),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.event}"



# Prijava na događaje
class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        permissions = [
            ("add_participation", "Can add participation"),
            ("view_participation", "Can view participation"),
        ]

    def __str__(self):
        return f"{self.participant} participating in {self.event}"
    


# Dodavanje slika ili dokumenta na događaje
class Attachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        permissions = [
            ("add_attachment", "Can add attachment"),
            ("view_attachment", "Can view attachment"),
        ]

    def __str__(self):
        return f"Attachment for {self.event}"
