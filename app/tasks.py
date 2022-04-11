import os
import os.path
import pathlib
import shutil

from billiard.exceptions import SoftTimeLimitExceeded
from django.conf import settings
from django.utils import timezone

from .apis.cloudinary_api import upload_audio
from .celery import app
from .models import (SourceFile, TaskStatus,
                     YTAudioDownloadTask, SourceTrack, DynamicMix)
from .utils import get_valid_filename, save_dynamic_mix_copy
from .youtubedl import download_audio, get_file_ext

"""
This module defines various Celery tasks used for Spleeter Web.
"""


@app.task(autoretry_for=(Exception,),
          default_retry_delay=3,
          retry_kwargs={'max_retries': settings.YOUTUBE_MAX_RETRIES})
def fetch_youtube_audio(source_file_id, source_track_id, fetch_task_id, artist, title, link):
    try:
        source_file = SourceFile.objects.get(id=source_file_id)
    except SourceFile.DoesNotExist:
        print('SourceFile does not exist')
        return
    try:
        source_track = SourceTrack.objects.get(id=source_track_id)
    except SourceFile.DoesNotExist:
        print('SourceTrack does not exist')
        return
    fetch_task = YTAudioDownloadTask.objects.get(id=fetch_task_id)
    fetch_task.status = TaskStatus.IN_PROGRESS
    fetch_task.save()

    try:
        directory = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR,
                                 str(source_file_id))
        filename = str(get_valid_filename(get_valid_filename(artist) + '-' +
                                          get_valid_filename(title)) + get_file_ext(link)).strip()
        rel_media_path = os.path.join(settings.UPLOAD_DIR, str(source_file_id),
                                      filename)
        rel_path = os.path.join(settings.MEDIA_ROOT, rel_media_path)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        # Start download
        download_audio(link, rel_path)

        # Check file exists
        if os.path.exists(rel_path):
            fetch_task.status = TaskStatus.DONE
            fetch_task.date_finished = timezone.now()
            path_on_cloudinary = 'musicas' + '/' + filename
            req = upload_audio(rel_path, path_on_cloudinary)
            source_file.file_url = req['url']
            source_file.public_id = req['public_id']
            source_file.duration = req['duration']
            source_file.filename = filename
            os.remove(rel_path)
            directory = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR,
                                     source_file_id)
            shutil.rmtree(directory, ignore_errors=True)
            fetch_task.save()
            source_file.save()
            create_dynamic_mix(source_track)
        else:
            raise Exception('Error writing to file')
    except SoftTimeLimitExceeded:
        print('Aborted!')
    except Exception as error:
        print(error)
        fetch_task.status = TaskStatus.ERROR
        fetch_task.date_finished = timezone.now()
        fetch_task.error = str(error)
        fetch_task.save()
        raise error


@app.task()
def fetch_upload_audio(source_file_id, source_track_id, fetch_task_id, artist, title, link):
    pass


def create_dynamic_mix(source_track):
    qs = DynamicMix.objects.filter(source_track__source_file__file_url=source_track.source_file.file_url,
                                   status=TaskStatus.DONE)
    if qs.exists():
        dynamic_on_db = qs.first()
        dynamic = DynamicMix()
        dynamic.source_track = source_track
        dynamic.separator = dynamic_on_db.separator
        dynamic.separator_args = dynamic_on_db.separator_args
        dynamic.bitrate = dynamic_on_db.bitrate
        save_dynamic_mix_copy(dynamic, dynamic_on_db)
    else:
        dynamic = DynamicMix()
        dynamic.source_track = source_track
        dynamic.save()
