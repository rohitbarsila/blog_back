from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STAT = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('hidden', 'Hidden'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('user','User'),
        ('admin','Admin')
    )
    user_type = models.CharField(max_length=50, default='user', choices=TYPE_CHOICES, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        return str(self.user)


class tags(models.Model):
    name=models.CharField(max_length=30)
    frequency=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class post(models.Model):
    name=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title=models.CharField(max_length=100 ,unique=True)
    content=models.TextField()
    status=models.CharField( choices=STAT,default='pending',max_length=10)
    tag=models.ManyToManyField(tags,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.title)

class comment(models.Model):
    name=models.ForeignKey(post,on_delete=models.CASCADE)
    comment=models.TextField()
    status=models.CharField( choices=STAT,default='pending',max_length=10)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)


