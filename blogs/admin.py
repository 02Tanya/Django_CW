from django.contrib import admin

from blogs.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "body")
    search_fields = ("title",)
