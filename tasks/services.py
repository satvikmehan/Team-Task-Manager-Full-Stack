from .models import Task
from projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

def create_task(data, request_user):
    try:
        project = Project.objects.get(id=data['project_id'])
    except Project.DoesNotExist:
        return None, "Project not found"

    try:
        assigned_user = User.objects.get(id=data['assigned_to'])
    except User.DoesNotExist:
        return None, "User not found"

    # 🔒 Check user is member of project
    if assigned_user not in project.members.all():
        return None, "User is not a project member"

    task = Task.objects.create(
        title=data['title'],
        description=data.get('description', ''),
        project=project,
        assigned_to=assigned_user,
        created_by=request_user
    )

    return task, None