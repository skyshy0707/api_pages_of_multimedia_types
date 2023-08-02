from django.db import models
from model_utils.managers import InheritanceManager
import os

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
# Create your models here.

class Page(models.Model):

    title = models.CharField(verbose_name="Заголовок", max_length=1000)

    def get_detail_page(self,):
        return f"{BASE_URL}/api/page/{self.id}/detail"

class Content(models.Model):

    title = models.CharField(verbose_name="Заголовок", max_length=1000)
    pages = models.ManyToManyField(Page, verbose_name="Страницы", blank=True, default=[])
    view_count = models.BigIntegerField(verbose_name="Счётчик просмотров", default=0)

    objects = InheritanceManager()

    def __str__(self):
        return self.title

class Audio(Content):

    bitrate = models.IntegerField(verbose_name="Битрейт, Бит/с")

class Text(Content):

    content = models.TextField(verbose_name="Текст", max_length=5000)

class Video(Content):

    file_link = models.URLField(verbose_name="Ссылка на файл видео")
    subtitles_link = models.URLField(verbose_name="Ссылка на файл субтитров", blank=True, null=True)