from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .services import create_user


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('/api/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            return render(request, 'signup.html', {
                'error': 'Username and password are required.'
            })

        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'This username already exists.'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('/login/?created=1')

    return render(request, 'signup.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/api/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {
                'error': 'Invalid username or password.'
            })

        login(request, user)
        return redirect('/api/')

    return render(request, 'login.html', {
        'success': 'Account created. You can log in now.'
        if request.GET.get('created') == '1' else ''
    })


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def signup_view(request):
    try:
        user = create_user(request.data)
        return Response({
            "message": "User created successfully",
            "username": user.username,
            "role": user.role
        }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        tokens = get_tokens_for_user(user)

        return Response({
            "message": "Login successful",
            "username": user.username,
            "role": user.role,
            "tokens": tokens
        })

    return Response({"error": "Invalid credentials"}, status=401)


@api_view(['PATCH'])
def change_role(request, user_id):
    if not request.user.is_superuser:
        return Response({"error": "Only superuser allowed"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.role = request.data.get('role')
        user.save()

        return Response({"message": "Role updated"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
