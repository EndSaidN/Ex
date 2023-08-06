from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Post, Profile, Comment

admin.site.unregister(Group)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Post)
