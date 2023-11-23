from authentication.serializers import CustomRegisterSerializer, CustomNodeRegistrationSerializer, CustomJWTSerializer
from dj_rest_auth.registration.views import RegisterView


class RegistrationView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomNodeRegistrationView(RegisterView):
    serializer_class = CustomNodeRegistrationSerializer

    def get_response_data(self, user):
        return CustomJWTSerializer(user, context=self.get_serializer_context()).data
