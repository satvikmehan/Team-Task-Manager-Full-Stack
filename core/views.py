from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "message": "Task Manager API is running"
    })
