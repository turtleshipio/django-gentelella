from django.template import Library
from app.models import TCGroup
register = Library()

@register.filter()
def check_permission(user, perm):
    return user.has_perm(permission)

@register.filter()
def check_group(user, group):
    return user.groups.filter(name=group).exists()

