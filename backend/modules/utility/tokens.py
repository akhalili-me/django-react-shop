from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return token


def apply_jwt_token_credentials_to_client(client, user):
    tokens = generate_jwt_token(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
