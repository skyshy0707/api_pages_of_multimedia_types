import logging
import os

from celery import shared_task

from . import models

logger = logging.getLogger("django")

@shared_task
def plus_single_view(id):
    try:
        content = models.Content.objects.get(pk=id)
        content.view_count += 1
        content.save()
    except models.Content.DoesNotExist:
        logger.warning(f"Контент с id={id} был удалён")
    return "Done"