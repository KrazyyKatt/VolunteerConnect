from django.core.management.base import BaseCommand
from main.models import CustomUser, Event, Comment, Participation, Attachment
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Popunjava bazu podataka testnim podacima"

    def handle(self, *args, **kwargs):
        # Kreiraj korisnike
        self.stdout.write("Kreiranje korisnika...")
        for i in range(5):
            CustomUser.objects.create_user(
                username=f"user{i+1}",
                email=f"user{i+1}@example.com",
                password="password123",
                phone_number=f"123-456-78{i+1}",
                address=f"Ulica {i+1}, Grad"
            )

        users = CustomUser.objects.all()

        # Kreiraj događaje
        self.stdout.write("Kreiranje događaja...")
        for i in range(10):
            Event.objects.create(
                title=f"Događaj {i+1}",
                description="Opis događaja",
                date=timezone.now(),
                location=f"Lokacija {i+1}",
                organizer=random.choice(users),
            )

        events = Event.objects.all()

        # Kreiraj komentare
        self.stdout.write("Kreiranje komentara...")
        for event in events:
            for _ in range(3):
                Comment.objects.create(
                    event=event,
                    author=random.choice(users),
                    content="Ovo je testni komentar.",
                )

        # Kreiraj sudionike
        self.stdout.write("Kreiranje sudionika...")
        for event in events:
            for _ in range(2):
                Participation.objects.create(
                    event=event,
                    participant=random.choice(users),
                )

        # Kreiraj priloge
        self.stdout.write("Kreiranje priloga...")
        for event in events:
            Attachment.objects.create(
                event=event,
                file="attachments/test_file.pdf"
            )

        self.stdout.write(self.style.SUCCESS("Baza je uspješno popunjena testnim podacima!"))