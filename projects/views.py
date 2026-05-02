from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import create_project
from .models import Project
from .services import add_members_to_project

from django.shortcuts import render
from .models import Project

from django.shortcuts import redirect

from django.contrib.auth.models import User

from accounts.utils import admin_required

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_protected(request):
    return Response({
        "message": "You are authenticated",
        "user": request.user.username,
        "role": request.user.role
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project_view(request):

    # 🔒 RBAC: only admin allowed
    if request.user.role != 'ADMIN':
        return Response({"error": "Only admin can create project"}, status=403)

    project = create_project(request.data, request.user)

    return Response({
        "message": "Project created",
        "project": project.name
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.filter(members=request.user)

    data = []
    for p in projects:
        data.append({
            "id": p.id,
            "name": p.name,
            "owner": p.owner.username
        })

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_members_view(request, project_id):

    # 🔒 Only ADMIN can add members
    if request.user.role != 'ADMIN':
        return Response({"error": "Only admin can add members"}, status=403)

    user_ids = request.data.get('user_ids', [])

    project, error = add_members_to_project(project_id, user_ids, request.user)

    if error:
        return Response({"error": error}, status=400)

    return Response({
        "message": "Members added successfully",
        "project": project.name,
        "members": [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        } for user in project.members.all()
]
})

def project_list_page(request):
    user = request.user

    if getattr(user, 'role', None) == 'ADMIN':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(members=user)

    return render(request, "projects.html", {"projects": projects})

@admin_required
def create_project_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("description")

        Project.objects.create(
            name=name,
            description=desc,
            owner=request.user
        )

        return redirect("/projects/")

    return render(request, "create_project.html")

@admin_required
def add_members_page(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        project.members.add(user)

    return render(request, "add_members.html")