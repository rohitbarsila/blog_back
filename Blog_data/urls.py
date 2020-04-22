from django.contrib import admin
from django.urls import path,include
from .views import login,posts,register,comment
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('heroes',views.HeroViewSet)

urlpatterns = [
    path('api/login', login),
    path('api/register', register),
    path('api/post', posts),
    path('api/comment', comment),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
