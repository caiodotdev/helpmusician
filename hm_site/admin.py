from django.contrib import admin

# Register your models here.
from hm_site.models import Post


class PostAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'filename',
    )
    list_display = ('id', 'title', 'slug', 'author', 'status', 'created_at',)


admin.site.register(Post, PostAdmin)
