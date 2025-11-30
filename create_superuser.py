import os
from django.contrib.auth import get_user_model

def run():
    if os.getenv("SUPERUSER_CREATE") != "true":
        print("SUPERUSER_CREATE not enabled.")
        return

    email = os.getenv("SUPERUSER_EMAIL")
    password = os.getenv("SUPERUSER_PASSWORD")

    if not email or not password:
        print("Missing SUPERUSER_EMAIL or SUPERUSER_PASSWORD.")
        return

    User = get_user_model()

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)
        print(f"Superuser created: {email}")
    else:
        print(f"Superuser already exists: {email}")
