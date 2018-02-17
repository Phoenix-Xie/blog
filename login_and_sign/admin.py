# Register your models here.

from django.contrib import admin
from django.contrib.admin import actions
from .models import User

# admin.site.disable_action('delete_selected')


actions.delete_selected.short_description = '删除所选项'


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)