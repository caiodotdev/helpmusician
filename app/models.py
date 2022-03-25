from django.db import models

# Create your models here.

# Create your models here.
class Music(models.Model):
    youtube_url = models.URLField(blank=True, null=True)
    chordInfo = models.CharField(max_length=255, blank=True, null=True)
    derivedKey = models.CharField(max_length=255, blank=True, null=True)
    derivedBpm = models.CharField(max_length=255, blank=True, null=True)
    barLength = models.CharField(max_length=255, blank=True, null=True)
    versionId = models.CharField(max_length=255, blank=True, null=True)
    chords = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
