from django.contrib import admin

from .models import NewsleterAccount


class NewsleterAdmin(admin.ModelAdmin):

    list_display = ('email', 'added_at')
    search_fields = ['email']


admin.site.register(NewsleterAccount, NewsleterAdmin)
