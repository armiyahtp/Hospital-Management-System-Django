import os
from django.contrib.auth import get_user_model

def run():
    if os.getenv("SUPERUSER_CREATE") != "true":
        return
    
    email = os.getenv("SUPERUSER_EMAIL")
    password = os.getenv("SUPERUSER_PASSWORD")

    if not email or not password:
        print("Superuser env vars missing.")
        return
    
    User = get_user_model()
    
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)
        print("Superuser created: ", email)
    else:
        print("Superuser already exists.")
