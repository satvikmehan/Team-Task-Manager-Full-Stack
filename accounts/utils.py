from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('/')

        if getattr(user, 'role', None) != 'ADMIN':
            return redirect('/dashboard/')

        return view_func(request, *args, **kwargs)

    return wrapper