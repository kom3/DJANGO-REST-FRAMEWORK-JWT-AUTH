import re

from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.conf import settings


class myMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if hasattr(settings, "EXCLUDE_URLS"):
            self.exclude_urls = [re.compile(url) for url in settings.EXCLUDE_URLS]

    def __call__(self, request):
        response = self.get_response(request)
        print("\n\nI am a custom middleware...\n")
        print("path info:", request.path_info)
        return response

    # @method_decorator(login_required)
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated or any(url.match(request.path_info) for url in self.exclude_urls):
            print("YES>>>>>Excempt url")
            pass
        else:
            # return redirect(settings.LOGIN_URL)
            return login_required(view_func)(request, view_args, view_kwargs)


