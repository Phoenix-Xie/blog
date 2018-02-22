# Register your models here.
from django.contrib import admin

from .models import Passage, Comment

admin.DateFieldListFilter.title = '按出版时间'
# admin.DateFieldListFilter


class PassageAdmin(admin.ModelAdmin):
    list_filter = ('pub_time',)


admin.site.register(Passage, PassageAdmin)
admin.site.register(Comment)
