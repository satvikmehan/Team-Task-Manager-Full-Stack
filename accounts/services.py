from .models import User

def create_user(data):
    user = User.objects.create_user(
        username=data['username'],
        password=data['password'],
        role='MEMBER'
    )
    return user