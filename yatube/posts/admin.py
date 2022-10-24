from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'created', 'author', 'group')
    # Изменять поле групп
    list_editable = ('group',)
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('created',)
    # Если нет постов
    empty_value_display = '-пусто-'


admin.site.register(Group)
admin.site.register(Post, PostAdmin)
