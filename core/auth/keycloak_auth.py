import requests
from jose import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.models import User


class KeycloakAuthentication(BaseAuthentication):
    """
    Authenticate requests using Keycloak-issued access tokens
    (Direct Access Grant / Password Flow compatible)
    """

    def authenticate(self, request):
        # =========================
        # 1. Read Authorization header
        # =========================
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # DRF will treat user as anonymous

        token = auth_header.split(" ", 1)[1]

        # =========================
        # 2. Fetch Keycloak JWKS
        # =========================
        jwks_url = (
            f"{settings.KEYCLOAK_SERVER_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}"
            f"/protocol/openid-connect/certs"
        )
        print("\n==== AUTH DEBUG START ====")
        print("AUTH HEADER:", auth_header)
        print("KEYCLOAK_SERVER_URL:", settings.KEYCLOAK_SERVER_URL)
        print("REALM:", settings.KEYCLOAK_REALM)

        try:
            jwks = requests.get(jwks_url, timeout=5).json()
        except Exception:
            raise AuthenticationFailed("Unable to fetch Keycloak public keys")

        # =========================
        # 3. Find signing key
        # =========================
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header["kid"]
            key = next(k for k in jwks["keys"] if k["kid"] == kid)
        except Exception:
            raise AuthenticationFailed("Invalid token signing key")

        # =========================
        # 4. Decode & verify token
        # =========================
        try:
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                issuer=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}",
                options={
                    "verify_aud": False,  # IMPORTANT for Keycloak password flow
                },
            )
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        # =========================
        # 5. Validate client (azp)
        # =========================
        azp = payload.get("azp")
        if azp != settings.KEYCLOAK_CLIENT_ID:
            raise AuthenticationFailed("Invalid token client")

        # =========================
        # 6. Extract user identity
        # =========================
        email = payload.get("email")
        if not email:
            raise AuthenticationFailed("Email missing in token")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "is_active": True,
                "username": payload.get("preferred_username", email),
            },
        )

        return (user, token)

