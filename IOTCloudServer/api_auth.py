from ninja.security import HttpBearer, APIKeyHeader
from core.models import ExpirableToken, ApiKey
from django.utils import timezone
from typing import Optional

class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = ExpirableToken.objects.get(token=token)
            if token_obj.is_expired:
                return None
            return token_obj.user
        except ExpirableToken.DoesNotExist:
            return None

class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if not key:
            return None
            
        try:
            api_key = ApiKey.objects.get(key=key)
            if not api_key.never_expires and api_key.expiry < timezone.now():
                return None
            return api_key.owner
        except ApiKey.DoesNotExist:
            return None

# Multiple authenticators using list
class GlobalAuth:
    def __init__(self):
        self.auth_handlers = [BearerAuth(), ApiKeyAuth()]

    def __call__(self, request):
        # Try each auth method in sequence
        for auth in self.auth_handlers:
            user = auth(request)
            if user is not None:
                return user
        return None

def add_authenticated_user(request, call_next):
    user, token = request.auth
    if user is not None:
        request.auth = user
    response = call_next(request)
    return response

from ninja.security import HttpBearer
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = User.objects.get(auth_token=token)
            return user
        except User.DoesNotExist:
            return None
