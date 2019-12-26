"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from apps.users.views import LoginEmailAPI, LoginFacebookAPI

schema_view = get_swagger_view(title='Travel API docs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_docs/', schema_view),
    path('auth/login_email/', LoginEmailAPI.as_view({'post': 'post'})),
    path('auth/login_fb/', LoginFacebookAPI.as_view({'post': 'post'})),
    path('category/', include('apps.category.urls')),
    path('questions/', include('apps.questions.urls')),
    path('answers/', include('apps.answers.urls')),
    path('comments/', include('apps.comments.urls')),
]
