from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from app.apis.cloudinary_api import remove_cloudinary_file
from app.models import DynamicMix, SourceFile, SourceTrack, StaticMix

"""
This module defines pre- and post-delete signals to ensure files are deleted when a model is deleted from the DB.
"""


@receiver(pre_delete,
          sender=SourceFile,
          dispatch_uid='delete_source_file_signal')
def delete_source_file(sender, instance, using, **kwargs):
    if str(instance.id):
        try:
            remove_cloudinary_file(instance.public_id)
        except (Exception,):
            print('SourceFile Signal delete: Nao conseguiu remover Musica do Cloudinary')


@receiver(post_delete,
          sender=SourceTrack,
          dispatch_uid='delete_source_track_signal')
def delete_source_track(sender, instance, using, **kwargs):
    print(instance.source_file)
    if instance.source_file:
        qs = SourceTrack.objects.filter(source_file__file_url=instance.source_file.file_url)
        print(qs)
        if qs.all().count() == 0:
            try:
                remove_cloudinary_file(instance.source_file.public_id)
            except (Exception,):
                print('SourceTrack Signal delete: Nao conseguiu remover Musica do Cloudinary')
            instance.source_file.delete()


@receiver(pre_delete,
          sender=StaticMix,
          dispatch_uid='delete_static_mix_signal')
def delete_static_mix(sender, instance, using, **kwargs):
    if str(instance.id):
        qs = StaticMix.objects.filter(file_url=instance.file_url)
        if qs.all().count() == 1:
            try:
                remove_cloudinary_file(instance.public_id)
            except (Exception,):
                print('StaticMix Signal delete:Nao conseguiu remover do Cloudinary')


@receiver(pre_delete,
          sender=DynamicMix,
          dispatch_uid='delete_dynamic_mix_signal')
def delete_dynamic_mix(sender, instance, using, **kwargs):
    if instance.vocals_url:
        qs = DynamicMix.objects.filter(vocals_url=instance.vocals_url)
        if qs.all().count() == 1:
            try:
                remove_cloudinary_file(instance.vocals_public_id)
                remove_cloudinary_file(instance.piano_public_id)
                remove_cloudinary_file(instance.other_public_id)
                remove_cloudinary_file(instance.bass_public_id)
                remove_cloudinary_file(instance.drums_public_id)
            except (Exception,):
                print('DynamicMix Signal delete:Nao conseguiu remover do Cloudinary')
