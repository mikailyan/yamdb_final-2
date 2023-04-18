from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreInline,)


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
