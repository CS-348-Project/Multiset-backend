from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    given_name = serializers.CharField(required=False)
    family_name = serializers.CharField(required=False)