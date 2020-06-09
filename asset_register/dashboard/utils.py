import functools

from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse


def login_required(api: bool = False):
    def _f(func):
        @functools.wraps(func)
        def _w(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            if not request.user.is_authenticated:
                # Dont redirect api requests to azure sso, it doest like it
                if api:
                    return JsonResponse(
                        {"error": "User unauthenticated, please refresh the page and try again"}, status=401
                    )
                return HttpResponseRedirect(reverse("oidc_authentication_init"))

            return func(request, *args, **kwargs)

        return _w

    return _f
