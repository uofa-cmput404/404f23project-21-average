from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    github = serializers.CharField(required=False,)
    host = serializers.CharField(required=False, read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
        
    # override get_cleaned_data of RegisterSerializer
    # def get_cleaned_data(self):
    #     super(CustomRegisterSerializer, self).get_cleaned_data()
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'password2': self.validated_data.get('password2', ''),
    #         'email': self.validated_data.get('email', ''),
    #         'github': self.validated_data.get('github', ''),
    #     }

    def custom_signup(self, request, user):
        user.github = self.validated_data.get('github', '')
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.host = request.build_absolute_uri()
        user.save()
        return user

    # override save method of RegisterSerializer
    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     user.username = self.cleaned_data.get('username')
    #     user.email = self.cleaned_data.get('email')
    #     user.github = self.cleaned_data.get('github')
    #     user.host = self.cleaned_data.get('host')
    #     user.save()
    #     adapter.save_user(request, user, self)
    #     return user