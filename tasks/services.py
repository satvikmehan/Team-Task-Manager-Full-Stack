from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

from projects.models import Project
from .models import Task

User = get_user_model()


def create_task(data, request_user):
    title = data.get('title', '').strip()
    if not title:
        return None, "Task title is required"

    try:
        project = Project.objects.get(id=data['project_id'])
    except (Project.DoesNotExist, KeyError, ValueError):
        return None, "Project not found"

    try:
        assigned_user = User.objects.get(id=data['assigned_to'])
    except (User.DoesNotExist, KeyError, ValueError):
        return None, "User not found"

    if not project.members.filter(id=assigned_user.id).exists():
        return None, "User is not a project member"

    status = data.get('status', 'TODO')
    if status not in dict(Task.STATUS_CHOICES):
        return None, "Invalid status"

    due_date = data.get('due_date')
    if due_date:
        due_date = parse_date(due_date)
        if due_date is None:
            return None, "Invalid due_date format. Use YYYY-MM-DD"

    task = Task.objects.create(
        title=title,
        description=data.get('description', ''),
        project=project,
        assigned_to=assigned_user,
        created_by=request_user,
        due_date=due_date,
        status=status
    )

    return task, None
