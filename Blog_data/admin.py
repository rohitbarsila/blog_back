from django.contrib import admin
from .models import UserProfile,tags,post,comment


class postAdmin(admin.ModelAdmin):
    resource_class = post
    # readonly_fields=('created','modified',)
    list_display = ('name', 'title', 'status', 'modified')

class tagAdmin(admin.ModelAdmin):
    resource_class = post
    # readonly_fields=('created','modified',)
    list_display = ('name', 'frequency','modified')

class userProfileAdmin(admin.ModelAdmin):
    resource_class = post
    # readonly_fields=('created','modified',)
    list_display = ('user', 'user_type')

class commentAdmin(admin.ModelAdmin):
    resource_class = post
    # readonly_fields=('created','modified',)
    list_display = ('name', 'comment', 'status', 'modified')

admin.site.register(UserProfile,userProfileAdmin)
admin.site.register(tags,tagAdmin)
admin.site.register(post,postAdmin)
admin.site.register(comment,commentAdmin)

