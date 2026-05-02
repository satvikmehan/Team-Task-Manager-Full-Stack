from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

def add_members_to_project(project_id, user_ids, request_user):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return None, "Project not found"

    # 🔒 Only owner can modify project
    if project.owner != request_user:
        return None, "Only project owner can add members"

    users = User.objects.filter(id__in=user_ids)

    if not users.exists():
        return None, "No valid users found"

    project.members.add(*users)

    return project, None

def create_project(data, user):
    project = Project.objects.create(
        name=data['name'],
        description=data.get('description', ''),
        owner=user
    )

    # add owner as member by default
    project.members.add(user)

    return project