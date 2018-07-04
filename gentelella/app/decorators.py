from django.http import HttpResponseForbidden, HttpResponseBadRequest


def ajax_required(f):

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def can_manage_ws():
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if not request.user.has_tcperm('change_wsbytcgroup'):
                return HttpResponseForbidden
            else:
                return function(request, *args, **kwargs)
        return wrap
    return decorator


