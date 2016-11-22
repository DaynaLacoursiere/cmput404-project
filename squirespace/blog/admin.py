from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment, Squire

admin.site.register(Comment)
admin.site.register(Post)

def admin_approval(modeladmin, request, queryset):
	queryset.update(is_active=True)
admin_approval.short_description = "Approve User"

class SquireInline(admin.StackedInline):
    model = Squire
    verbose_name = 'Squire'

# Don't use this until we better understand why and how.
class SquireAdmin(admin.ModelAdmin):
	model = Squire
	list_display= ['theUUID']
	ordering = ['is_active']
	actions = [admin_approval]

class UserAdmin(admin.ModelAdmin):
	list_display= ['username', 'is_active']
	ordering = ['is_active']
	actions = [admin_approval]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Squire)
#admin.site.register(Squire, SquireAdmin)
