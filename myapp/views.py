# using rest framework model serializer wecan seralize query set to primitive data type
from rest_framework_jwt.settings import api_settings
from .serializers import TokenSerializer
# django serialize to serialize query set
from django.core.serializers import serialize
import json
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets

from rest_framework.views import APIView

from django.views import View

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from .models import Mymodel

# Create your views here.


def helloview(request):
    return HttpResponse("<h2>I am 'hello' API</h2>")


class myTemplateView(TemplateView):
    template_name = "myapp/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mydata'] = "MyDataVariable_Value_from_context"
        return context


class MyListView(ListView):
    model = Mymodel
    context_object_name = "names_list"  # default object_list
    paginate_by = 3  # http://127.0.0.1:7878/mylistview?page=2


def mySecureAPI(request):
    user = authenticate(username=request.user, password='test')
    if user is not None:
        return HttpResponse("<h1>User is authenticated, and he is accessing secured API</h2>")
    else:
        return HttpResponse("<h1>User is not authenticated</h2>")

# @login_required #or can use custom middleware to secure all apis


@login_required
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def myLoginview(request):
    JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
    JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
    payload = JWT_PAYLOAD_HANDLER(request.user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    print(jwt_token)
    resp = HttpResponse("<h3>My Home page</h3>")
    resp.set_cookie("Token", str(jwt_token), httponly=True)
    return resp


class HomeView(TemplateView):
    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


class ClassView(View):
    # @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, I am ClassView!<br><a href="logout">Logout</a>')


###################################################### USING REST FRAMEWORK AUTHENTICATION ####################################################


#############################################  BASIC AUTHENTICATION  ###############################################
# In basic authentication for ananymous user request.user will be ananynous and request.auth will be none
# In basic authentication for authenticated user request.user will be user instance  and request.auth will be none(in basic auth)

# class based

class MySecureClassAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        print(request.user, request.auth)
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return JsonResponse(content)

# funcion based


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def MySecureFunctionAPI(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return JsonResponse(content)
  #############################################################################################################################

##################################################### DRF TOKEN AUTHENTICATION #####################################################


################################################################################################################################
# In token authentication for ananymous user request.user will be ananynous and request.auth will be none
# In token authentication for authenticated user request.user will be user instance  and request.auth will be token(in token auth)

@login_required
def crateToken(request):
    token = Token.objects.filter(user=request.user)
    token = Token.objects.all()
    if token:
        # token = serialize('jsonl', token)
        # print(token)

        token = TokenSerializer(token, many=True)
        # print(token)
        print(token.data)
        # print(json.loads(token))
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            # 'auth': str(request.auth),  # None
        }
        print(content)

        return HttpResponse("Token generated for user %s: %s" % (request.user, json.dumps(token.data)))
    else:
        token = Token.objects.create(user=request.user)
        return HttpResponse(token.key)


############################################### JWT aunthentication #################################################

# 'rest_framework_simplejwt.authentication.JWTAuthentication', add this in REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': []} in settings.py

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class CheckForCustomPerm(BasePermission):
    def has_cust_permission(self, request, view):
        print("Checking for custon perms...")
        print(request.user)
        print(request.user.has_perms(["can_access_hello"]))
        return request.user.has_perms(["can_access_hello"])


class HelloView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]  //globally given
    # can also set IsAuthenticated globally in settings
    # permission_classes = [IsAuthenticated & CheckForCustomPerm]



    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        print(request.user)
        print(request.auth)
        content = {
            'status': 'request was permitted'
        }
        HttpResponse(str(content))
