from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Comment
from django.contrib.auth.models import User

admin.site.register(Comment)
admin.site.register(Post)

def admin_approval(modeladmin, request, queryset):
	queryset.update(is_active=True)
admin_approval.short_description = "Approve User"

class UserAdmin(admin.ModelAdmin):
	list_display= ['username', 'is_active']
	ordering = ['is_active']
	actions = [admin_approval]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)