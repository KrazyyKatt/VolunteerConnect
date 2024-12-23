from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    """
    Provjerava je li datoteka slika na temelju ekstenzije.
    """
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))