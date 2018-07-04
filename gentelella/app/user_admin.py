from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.forms import TCUserCreationForm

class TCUserAdmin(BaseUserAdmin):
    add_form = TCUserCreationForm
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('phone', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )