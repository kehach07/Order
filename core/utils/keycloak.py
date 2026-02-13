import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


# ======================================================
# KEYCLOAK TOKEN (SIGNIN)
# ======================================================
def get_keycloak_token(email: str, password: str) -> dict:
    """
    Authenticate user against Keycloak using Direct Grant.
    Returns access & refresh tokens.
    """

    url = (
        f"{settings.KEYCLOAK_SERVER_URL}/realms/"
        f"{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    )

    payload = {
        "grant_type": "password",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        # "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "username": email,
        "password": password,
    }

    res = requests.post(url, data=payload)

    if res.status_code != 200:
        raise AuthenticationFailed("Invalid email or password")

    return res.json()


# ======================================================
# ADMIN TOKEN (FOR USER MANAGEMENT)
# ======================================================
def get_admin_token() -> str:
    """
    Get admin access token from Keycloak master realm
    """

    url = f"{settings.KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token"

    payload = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": settings.KEYCLOAK_ADMIN_USERNAME,
        "password": settings.KEYCLOAK_ADMIN_PASSWORD,
    }

    res = requests.post(url, data=payload)

    if res.status_code != 200:
        raise AuthenticationFailed("Failed to authenticate Keycloak admin")

    return res.json()["access_token"]


# ======================================================
# CREATE KEYCLOAK USER (SIGNUP)
# ======================================================
def create_keycloak_user(email: str, password: str, full_name: str = "") -> None:
    """
    Creates a fully active Keycloak user
    """

    admin_token = get_admin_token()

    first_name = full_name.split(" ")[0] if full_name else ""
    last_name = " ".join(full_name.split(" ")[1:]) if full_name else ""

    user_payload = {
        "username": email,
        "email": email,
        "enabled": True,
        "emailVerified": True,
        "firstName": first_name,
        "lastName": last_name,
        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": False,
            }
        ],
    }

    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }

    res = requests.post(
        f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
        json=user_payload,
        headers=headers,
    )

    if res.status_code not in (201, 204):
        raise AuthenticationFailed("Failed to create user in Keycloak")


# ======================================================
# ENSURE USER EXISTS (SAFE SYNC)
# ======================================================
def ensure_keycloak_user(email: str, password: str, full_name: str = "") -> None:
    """
    Creates Keycloak user only if not already present.
    """

    admin_token = get_admin_token()

    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }

    # Check if user exists
    search_url = (
        f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/"
        f"{settings.KEYCLOAK_REALM}/users?username={email}"
    )

    res = requests.get(search_url, headers=headers)

    if res.status_code == 200 and res.json():
        return  # User already exists

    # Otherwise create user
    create_keycloak_user(email, password, full_name)
