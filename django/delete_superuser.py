from django.contrib.auth.models import User

def delete_superuser(username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"Successfully deleted superuser: {username}")
    except User.DoesNotExist:
        print(f"User {username} not found")

delete_superuser(input("Enter superuser name to delete: "))
