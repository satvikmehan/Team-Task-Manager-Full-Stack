from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .services import create_user

from django.shortcuts import render, redirect
import requests

BASE_URL = "https://web-production-b507d.up.railway.app"

def signup_page(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        res = requests.post(f"{BASE_URL}/accounts/signup/", json=data)

        if res.status_code == 200:
            return redirect('/login/')

    return render(request, "signup.html")


def login_page(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        res = requests.post(f"{BASE_URL}/accounts/login/", json=data)

        if res.status_code == 200:
            token = res.json().get("access")
            request.session['token'] = token
            return redirect('/dashboard/')

    return render(request, "login.html")

def dashboard_page(request):
    token = request.session.get('token')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(f"{BASE_URL}/tasks/dashboard/", headers=headers)

    return render(request, "dashboard.html", {"data": res.json()})

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