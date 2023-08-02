import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from settings.settings import (
    DJANGO_SUPERUSER_USERNAME, 
    DJANGO_SUPERUSER_EMAIL,
    DJANGO_SUPERUSER_PASSWORD
)

logger = logging.getLogger("django")

class Command(BaseCommand):

    help = u"Создаёт суперпользователя"

    def handle(self, *args, **kwargs):

        user = get_user_model()
        try:
            user.objects.create_superuser(
                DJANGO_SUPERUSER_USERNAME, 
                DJANGO_SUPERUSER_EMAIL,
                DJANGO_SUPERUSER_PASSWORD
            )
        except IntegrityError:
            logger.warning("Пользователь с таким {username} существует".format(username=DJANGO_SUPERUSER_USERNAME))