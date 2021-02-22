from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.exists():
                groups = request.user.groups.values_list('name', flat=True)
                print(groups)
                print('ROLES:' + str(allowed_roles))
                for group in groups:
                    if group in allowed_roles:
                        print(group in allowed_roles)
                        return view_func(request, *args, **kwargs)
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'expert':
            return redirect('home')

        if group in ('admin', 'primary_expert'):
            return view_func(request, *args, **kwargs)

    return wrapper_function

