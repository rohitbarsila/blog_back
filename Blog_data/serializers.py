from rest_framework import serializers
from .models import UserProfile,tags,post,comment
from django.contrib.auth.models import User

class Post(serializers.ModelSerializer):

    class Meta:
        model = post
        fields = '__all__' #('name', 'title','content','status','tag')