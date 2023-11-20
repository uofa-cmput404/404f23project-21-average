from authentication.serializers import CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView

class RegistrationView(RegisterView):
    serializer_class = CustomRegisterSerializer