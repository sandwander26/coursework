import time
from django.contrib.auth.models import User
from django.contrib.auth import login
import uuid
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            user_id = str(uuid.uuid4())
            user = User.objects.create_user(username=user_id)
            user.save()
            login(request, user)  # Логиним пользователя

        response = self.get_response(request)
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @method_decorator(ratelimit(key='ip', rate='60/m'))
    def __call__(self, request):
        response = self.get_response(request)
        return response