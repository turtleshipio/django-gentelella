from django.template import Library
from app.models import TCGroup
register = Library()

@register.filter()
def get_full_name(user):
    return user.get_full_name()