from django.contrib import admin

from .models import UserYamDb


@admin.register(UserYamDb)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'confirmation_code',
        'email',
        'role',
        'is_superuser',
        'bio',
        'first_name',
        'last_name'
    )
    list_editable = ('role',)
    search_fields = ('username', 'role',)
