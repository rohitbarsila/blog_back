from django.shortcuts import render
from .serializers import Post
from django.db import IntegrityError
from .models import UserProfile,tags,post,comment
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets

class HeroViewSet(viewsets.ModelViewSet):
    queryset = post.objects.all().order_by('name')
    serializer_class = Post


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    try:
        if 'username' and 'password' in request.data:
            user = User.objects.create(
                username=request.data['username']
            )
            user.set_password(request.data['password'])
            user.save()
            UserProfile.objects.create(user_type='user',user_id=user.id).save()
            return Response({'Status': 'Created'},
                            status=HTTP_200_OK)
        else:
            return Response({'Status': 'Failed', 'Message': "Username or Password or UserType Missing"},
                            status=HTTP_400_BAD_REQUEST)

    except IntegrityError:
        return Response({'Status': 'Failed','Message':"KeyError Object already exist"},
                        status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def posts(request):
    if request.data['process']=='get':
        get_post = post.objects.get(title=request.POST.get('title'))
        json = {'title': get_post.title
            , 'content': get_post.content
            , 'name': get_post.name
            , 'tag': get_post.tag}
        return Response(json, status=HTTP_200_OK)
    elif request.data['process']=='create':
        name = request.user
        title = request.data['title']
        content = request.data['content']
        tag = request.data['tags']
        if UserProfile.objects.get(user=request.user).user_type == 'admin':
            save=tags.objects.create(name=name,status='approved',title=title,content=content)
        else:
            save = tags.objects.create(name=name, title=title, content=content)
        for tg in tag:
            try:
                tags.objects.create(name=tg).save()
            except:
                obj=tags.objects.get(name=tg)
                obj.update(frequency=tags.objects.get(name=tg).frequency+1).save()
            save.objects.create(tag=tg)
        save.save()
        return Response({'Status': 'Created'}, status=HTTP_200_OK)

    elif request.data['process']=='update' or request.data['process']=='delete':
        title = request.data['title']
        if UserProfile.objects.get(user=request.user).user_type=='admin' or post.objects.get(title=title).name==request.user:
            if request.data['process'] == 'update':
                name = request.user
                content = request.data['content']
                tag = request.data['tags']
                updates= tags.objects.get(title=title)
                save = updates.objects.update(name=name, title=title, content=content)
                for tg in tag:
                    try:
                        tags.objects.create(name=tg).save()
                        save.objects.create(tag=tg)
                    except:
                        obj = tags.objects.get(name=tg)
                        obj.update(frequency=tags.objects.get(name=tg).frequency + 1).save()
                        save.objects.update(tag=tg)
                save.save()
            elif request.data['process'] == 'delete':
                delete=post.objects.get(title=title).delete()
                delete.save()
        return Response({'Status': 'Updated'},
                        status=HTTP_200_OK)
    else:
        return Response({"status":"failed","message":"invalid process"}, status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def comment(request):

    if 'comment' in request.data and request.data['process'] == 'create':
        comnt=request.data['comment']
        name=request.user
        create=comment.objects.create(comment=comnt,name=name)
        create.save()

    if UserProfile.objects.get(user=request.user).user_type == 'admin' or post.objects.get(comment=request.data['comment']).name == request.user:
        if 'comment' in request.data and request.data['process'] == 'delete':
            comnt=request.data['comment']
            create=comment.objects.get(comment=comnt).delete()
            create.save()