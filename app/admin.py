from django.contrib import admin

# Register your models here.
from app.models import Music


class MusicAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "youtube_url", "chordInfo", "derivedKey", "derivedBpm", "barLength", "versionId")


admin.site.register(Music, MusicAdmin)
