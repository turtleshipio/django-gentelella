from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from app import utils
from app.models import *


def require_token():
    def decorator(function):
        def wrap(request, *args, **kwargs):
            try:
                token = request.session['token']
                if token is not None:
                    return function(request, *args, **kwargs)
                else:
                    request.session.flush()
                    request.session.modified = True
                    return redirect('/')
            except KeyError:
                request.session.flush()
                request.session.modified = True
                return redirect('/')
            except:
                request.session.flush()
                request.session.modified = True
                return redirect('/')

        return wrap
    return decorator

def can_manage_ws():
    def decorator(function):
        def wrap(request, *args, **kwargs):
            try:
                token = request.session['token']
                token = utils.decode_token(token)
                acc_type = token['acc_type']
                user = None
                username = token['username']
                org_id = None

                if acc_type =="retail":
                    user = RetailUser.objects.get(username=username)
                    org_id = user.retailer_id
                if acc_type == "pickup":
                    user = PickupUser.objects.get(username=username)
                    org_id = user.pickteam_id


                if Permissions.objects.filter(org_id=org_id,policy_name="wholesale").exists():
                    return function(request, *args, **kwargs)
                else:
                    return redirect('/home/')


            except Exception as e:
                return redirect('/home/')
        return wrap
    return decorator


