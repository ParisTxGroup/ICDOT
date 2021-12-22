from contextlib import ExitStack

from django_scopes import scope, scopes_disabled

from bhot.utils.threadlocal import current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        with ExitStack() as stack:
            stack.enter_context(current_user(user))
            if user is None:
                pass
            elif user.is_superuser:
                stack.enter_context(scopes_disabled())
            else:
                stack.enter_context(scope(user=user))
            return self.get_response(request)
