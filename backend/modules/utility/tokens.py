from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return token