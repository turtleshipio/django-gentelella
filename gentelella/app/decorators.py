from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render


def require_token():
    def decorator(function):
        def wrap(request, *args, **kwargs):
            try:
                token = request.session['token']
                if token is not None:
                    return function(request, *args, **kwargs)
                else:
                    return redirect('/')
            except KeyError:
                request.session.flush()
                request.session.modified = True
                return redirect('/')

        return wrap
    return decorator
