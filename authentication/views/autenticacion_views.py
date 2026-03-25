from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers import LoginSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer