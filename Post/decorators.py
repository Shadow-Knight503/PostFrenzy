from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return redirect('Login')
    return wrapper_func


def allowed_user(allowed_role=None):
    if allowed_role is None:
        allowed_role = ['admin']

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to visit this page"
                                    "Please go back")
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('Home')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func