# Register your models here.
from django.contrib import admin

from .models import Passage

admin.DateFieldListFilter.title = '按出版时间'
# admin.DateFieldListFilter


class PassageAdmin(admin.ModelAdmin):
    list_filter = ('pub_time',)


admin.site.register(Passage, PassageAdmin)