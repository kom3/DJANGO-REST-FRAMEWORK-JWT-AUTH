"""advancedproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

from django.contrib.auth.views import LoginView

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("helloapi/", views.helloview),
    path("templateview/", views.myTemplateView.as_view()),
    path("mylistview/", views.MyListView.as_view()),
    path("mysecureapi/", views.mySecureAPI),
    path('myloginview/', views.myLoginview),
    path('login/', LoginView.as_view()),
    path("homeview/", views.HomeView.as_view(template_name="myapp/home.html")),
    path("classview/", views.ClassView.as_view()),
    path("securerestapiclass/", views.MySecureClassAPI.as_view()),
    path("securerestapifun/", views.MySecureFunctionAPI),
    path("gettoken/", views.crateToken),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello')
    ]
