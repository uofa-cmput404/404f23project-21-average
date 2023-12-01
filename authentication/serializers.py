from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import JWTSerializer
from rest_framework.serializers import ModelSerializer
import base64
from socialDistribution.models import Author
from django.conf import settings


class CustomRegisterSerializer(RegisterSerializer, ModelSerializer):
    github = serializers.CharField(required=False)
    host = serializers.CharField(required=False, read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    # Add condition for OPTIONALLY require admin approval
    # make is_active = False by default
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Author
        fields = ['username', 'password1', 'password2', 'github', 'host', 'first_name', 'last_name', 'is_active']
        optional_fields = ['github']

    def custom_signup(self, request, user):
        print(request)
        user.github = self.validated_data.get('github', '')
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.displayName = self.validated_data.get('username', '')
        user.host = settings.BASEHOST
        # user.save()
        return user


class CustomNodeRegistrationSerializer(RegisterSerializer, ModelSerializer):
    teamName = serializers.CharField(required=True)
    
    class Meta:
        model = Author
        fields = ['teamName', 'password1', 'password2']
    
    def custom_signup(self, request, user):
        user.username = self.validated_data.get('teamName', '')
        user.host = request.headers['Origin']
        user.type = 'node'

        token = user.username + ":" + self.validated_data.get('password1', '')
        user.github = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        user.save()
        return user


class CustomJWTSerializer(JWTSerializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the field 'email'.
    """
    access = serializers.SerializerMethodField(method_name='get_token')
    refresh = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    def get_token(self, obj):
        return obj.github

    def get_user(self, obj):
            """
            Required to allow using custom USER_DETAILS_SERIALIZER in
            JWTSerializer. Defining it here to avoid circular imports
            """
            # JWTUserDetailsSerializer = api_settings.USER_DETAILS_SERIALIZER

            # user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
            return 'user_data'
