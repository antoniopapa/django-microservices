from .services import UserService


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user = UserService.get('user/admin', headers=request.headers)
        except:
            user = None

        request.user_ms = user

        return self.get_response(request)
