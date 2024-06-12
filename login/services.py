from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from .serializers import AuthSerializer
from .utils import get_user_data

def handle_google_login(request, validated_data):
    try:
        user_data = get_user_data(validated_data)
    except ValidationError as e:
        return redirect(f"{settings.BASE_APP_URL}/error?message={str(e)}")
    except ValueError as e:  # Add this to catch issues like missing email
        return redirect(f"{settings.BASE_APP_URL}/error?message={str(e)}")

    # Ensure username and email are valid
    if not user_data.get('email'):
        return redirect(f"{settings.BASE_APP_URL}/error?message=Email is required for user creation.")

    # Find or create the user in the database
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'username': user_data['email'],  # Using email as username
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
        }
    )

    # Log the user in
    login(request, user)

    # Redirect to the application's base URL or any other post-login page
    return redirect(settings.BASE_APP_URL)
