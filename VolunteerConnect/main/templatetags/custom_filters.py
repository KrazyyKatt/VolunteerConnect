import os
from django import template

register = template.Library()

#@register.filter
#def is_image(file_url):
    #"""
    #Provjerava je li datoteka slika na temelju ekstenzije.
    #"""
    #return file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))



@register.filter
def is_image(file_path):
    """Provjerava je li datoteka slika na temelju ekstenzije."""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Ako je file_path objekt s atributom `name`, koristi ga
    if hasattr(file_path, 'name'):
        ext = os.path.splitext(file_path.name)[-1].lower()
    else:
        # Ako je file_path string
        ext = os.path.splitext(file_path)[-1].lower()

    return ext in valid_extensions