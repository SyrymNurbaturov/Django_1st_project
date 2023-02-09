from polls import views
import re
from polls.models import *
from django.contrib.auth.models import User

class OneAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = User.objects.filter(username = request.user.username).first()
        uc = UserChoices.objects.filter(user = user).all()
        if uc:
            param = [i.question for i in uc]
            request.param = param
            views.IndexView(request = request)
