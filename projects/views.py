from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Project
from .services import add_members_to_project, create_project

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


@login_required(login_url='/')
def create_project_page(request):
    if getattr(request.user, 'role', None) != 'ADMIN':
        return redirect('/dashboard/')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            return render(request, 'create_project.html', {
                'error': 'Project name is required.'
            })

        create_project({
            'name': name,
            'description': description,
        }, request.user)

        return redirect('/dashboard/?project_created=1')

    return render(request, 'create_project.html')
