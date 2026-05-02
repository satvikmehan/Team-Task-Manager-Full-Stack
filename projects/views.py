from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from .models import Project
from .services import add_members_to_project, create_project

User = get_user_model()


def admin_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')

        if getattr(request.user, 'role', None) != 'ADMIN':
            return redirect('/dashboard/')

        return view_func(request, *args, **kwargs)

    return wrapper

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


@admin_user_required
def create_project_page(request):
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


@admin_user_required
def project_manage_page(request):
    projects = (
        Project.objects
        .select_related('owner')
        .prefetch_related('members')
        .order_by('name')
    )

    return render(request, 'project_manage.html', {
        'projects': projects,
        'project_updated': request.GET.get('project_updated') == '1',
        'members_added': request.GET.get('members_added') == '1',
    })


@login_required(login_url='/')
def assigned_projects_page(request):
    projects = (
        Project.objects
        .filter(members=request.user)
        .select_related('owner')
        .prefetch_related('members')
        .order_by('name')
    )

    return render(request, 'assigned_projects.html', {
        'projects': projects,
    })


@admin_user_required
def edit_project_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            return render(request, 'edit_project.html', {
                'project': project,
                'error': 'Project name is required.'
            })

        project.name = name
        project.description = description
        project.save()

        return redirect('/projects/manage/?project_updated=1')

    return render(request, 'edit_project.html', {
        'project': project
    })


@admin_user_required
def project_members_page(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related('members'),
        id=project_id
    )

    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')

        if not user_ids:
            return redirect(f'/projects/{project.id}/members/')

        users = User.objects.filter(id__in=user_ids)
        project.members.add(*users)

        return redirect('/projects/manage/?members_added=1')

    current_member_ids = project.members.values_list('id', flat=True)
    available_users = User.objects.exclude(id__in=current_member_ids).order_by('username')

    return render(request, 'project_members.html', {
        'project': project,
        'available_users': available_users,
    })
