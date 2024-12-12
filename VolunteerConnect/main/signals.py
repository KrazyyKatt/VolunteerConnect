from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created: 

        instance.user_permissions.clear()

        try:
            user_group = Group.objects.get(name='Users')
            instance.groups.add(user_group)
        except Group.DoesNotExist:
            print("The 'Users' group does not exist. Please create it in the admin panel.")