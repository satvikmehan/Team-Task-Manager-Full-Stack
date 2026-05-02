from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import create_task
from .models import Task

from datetime import date
from .models import Task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task_view(request):

    # 🔒 Only admin can create tasks
    if request.user.role != 'ADMIN':
        return Response({"error": "Only admin can create tasks"}, status=403)

    task, error = create_task(request.data, request.user)

    if error:
        return Response({"error": error}, status=400)

    return Response({
        "message": "Task created",
        "task": task.title
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    # 🔒 Only assigned user can update
    if request.user != task.assigned_to:
        return Response({"error": "Not allowed"}, status=403)

    new_status = request.data.get('status')

    if new_status not in ['TODO', 'IN_PROGRESS', 'DONE']:
        return Response({"error": "Invalid status"}, status=400)

    task.status = new_status
    task.save()

    return Response({
        "message": "Status updated",
        "task": task.title,
        "status": task.status
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):

    tasks = Task.objects.filter(assigned_to=request.user)

    data = []
    for t in tasks:
        data.append({
            "id": t.id,
            "title": t.title,
            "project": t.project.name,
            "status": t.status
        })

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):

    user = request.user

    tasks = Task.objects.filter(assigned_to=user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='DONE').count()
    pending_tasks = tasks.exclude(status='DONE').count()

    # overdue = due_date passed & not completed
    overdue_tasks = tasks.filter(
        due_date__lt=date.today()
    ).exclude(status='DONE').count()

    return Response({
    "total_tasks": total_tasks,
    "completed_tasks": completed_tasks,
    "pending_tasks": pending_tasks,
    "overdue_tasks": overdue_tasks,
    "status_breakdown": {
        "todo": tasks.filter(status='TODO').count(),
        "in_progress": tasks.filter(status='IN_PROGRESS').count(),
        "done": completed_tasks
    }
})