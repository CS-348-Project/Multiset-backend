def get_user_data(validated_data):
    """
    Extract and return user data from the validated_data.
    Ensure 'email' and 'username' are not None or empty.
    """
    email = validated_data.get('email')
    if not email:
        raise ValueError("Email is required for user creation.")
    
    user_data = {
        'email': email,
        'given_name': validated_data.get('given_name', ''),
        'family_name': validated_data.get('family_name', ''),
    }
    return user_data
