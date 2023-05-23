from django.contrib import admin
from .models import Email, Url


class EmailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Email, EmailsAdmin)
admin.site.register(Url, EmailsAdmin)
