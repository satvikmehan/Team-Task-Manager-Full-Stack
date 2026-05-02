from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .services import create_user

from django.shortcuts import render, redirect

from tasks.models import Task

BASE_URL = "https://web-production-b507d.up.railway.app"

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "User exists"})

        User.objects.create_user(username=username, password=password)

        return redirect('/')

    return render(request, "signup.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            request.session['user_id'] = user.id
            return redirect('/dashboard/')

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def dashboard_page(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/')

    tasks = Task.objects.filter(assigned_to_id=user_id)

    data = {
        "total_tasks": tasks.count(),
        "completed_tasks": tasks.filter(status='DONE').count(),
        "pending_tasks": tasks.exclude(status='DONE').count(),
    }

    return render(request, "dashboard.html", {"data": data})


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