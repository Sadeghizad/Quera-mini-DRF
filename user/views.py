from dj_rest_auth.views import PasswordResetConfirmView
from .serializers import CustomLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        # Validate the user credentials
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the JWT tokens along with user information
        return Response({
            'refresh': str(refresh),
            'access': access_token,
        })
    


def password_reset_confirm_view(request, *args, **kwargs):
    return PasswordResetConfirmView.as_view()(request, *args, **kwargs)