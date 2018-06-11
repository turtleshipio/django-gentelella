from app.models import TCGroup

def check_permission(user, perm):
    return user.has_perm(permission)

def check_group(user, group):
    return user.groups.filter(name=group).exists()


