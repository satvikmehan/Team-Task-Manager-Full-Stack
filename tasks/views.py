from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from .models import Task
from .services import create_task
from projects.models import Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()


def admin_required_page(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')

        if getattr(request.user, 'role', None) != 'ADMIN':
            return redirect('/dashboard/')

        return view_func(request, *args, **kwargs)

    return wrapper


def task_form_context(error=None, task=None):
    return {
        'error': error,
        'task': task,
        'projects': Project.objects.prefetch_related('members').order_by('name'),
        'users': User.objects.order_by('username'),
        'statuses': Task.STATUS_CHOICES,
    }


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


@admin_required_page
def create_task_page(request):
    if request.method == 'POST':
        task, error = create_task(request.POST, request.user)

        if error:
            return render(request, 'task_form.html', task_form_context(error=error))

        return redirect('/tasks/manage/?task_created=1')

    return render(request, 'task_form.html', task_form_context())


@admin_required_page
def manage_tasks_page(request):
    tasks = (
        Task.objects
        .select_related('project', 'assigned_to', 'created_by')
        .order_by('status', 'due_date', '-created_at')
    )

    return render(request, 'task_manage.html', {
        'tasks': tasks,
        'task_created': request.GET.get('task_created') == '1',
        'task_updated': request.GET.get('task_updated') == '1',
        'task_deleted': request.GET.get('task_deleted') == '1',
    })


@admin_required_page
def edit_task_page(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')

        if not title:
            return render(request, 'task_form.html', task_form_context(
                error='Task title is required.',
                task=task,
            ))

        if status not in dict(Task.STATUS_CHOICES):
            return render(request, 'task_form.html', task_form_context(
                error='Invalid status.',
                task=task,
            ))

        project = get_object_or_404(Project, id=request.POST.get('project_id'))
        assigned_user = get_object_or_404(User, id=request.POST.get('assigned_to'))

        if not project.members.filter(id=assigned_user.id).exists():
            return render(request, 'task_form.html', task_form_context(
                error='User is not a project member.',
                task=task,
            ))

        parsed_due_date = None
        if due_date:
            parsed_due_date = parse_date(due_date)
            if parsed_due_date is None:
                return render(request, 'task_form.html', task_form_context(
                    error='Invalid due_date format. Use YYYY-MM-DD.',
                    task=task,
                ))

        task.title = title
        task.description = description
        task.project = project
        task.assigned_to = assigned_user
        task.status = status
        task.due_date = parsed_due_date
        task.save()

        return redirect('/tasks/manage/?task_updated=1')

    return render(request, 'task_form.html', task_form_context(task=task))


@admin_required_page
def delete_task_page(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('/tasks/manage/?task_deleted=1')

    return render(request, 'task_confirm_delete.html', {
        'task': task
    })


@login_required(login_url='/')
def update_task_status_page(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.assigned_to:
        return redirect('/dashboard/')

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in dict(Task.STATUS_CHOICES):
            task.status = status
            task.save()

    return redirect('/dashboard/?task_status_updated=1')


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
