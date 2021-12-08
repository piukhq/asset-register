import functools

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse


def login_required(api: bool = False):
    def _f(func):
        @functools.wraps(func)
        def _w(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            authed = request.user.is_authenticated
            err_response = HttpResponseRedirect(reverse("oidc_authentication_init"))

            if api:
                err_response = JsonResponse(
                    {"error": "User unauthenticated, please refresh the page and try again"}, status=401
                )

                # Cheapo api auth for now
                if request.headers.get("Authorization", "").endswith("7bb4810d-6af0-484d-9595-3402c75bfdc3"):
                    authed = True

            if not authed:
                return err_response
            return func(request, *args, **kwargs)

        return _w

    return _f
