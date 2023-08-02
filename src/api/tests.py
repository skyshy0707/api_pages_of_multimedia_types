import os
import time

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase, override_settings

from . import models

API_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000") + "/api"

class APIMultimediaTestCase(APITestCase):

    def setUp(self):
        page = models.Page.objects.create(title="Future Breeze - Why Don't You Dance With Me? [1996]")
        description = models.Text.objects.create(
            title="Описание", 
            content="Это дебютный сингл Future Breeze, музыку из которого многие задействуют и по сей день "\
                    "на заставки для оформления видеороликов. Когда-то и он в конце 90-х занимал первые строчки хит-парадов."
        )
        info = models.Text.objects.create(title="Информация", content="Год: 1996, Лейбл: PolyGram Records Pty. Limited")
        track01 = models.Audio.objects.create(title="Why Don't You Dance With Me (Sequential One Airplay Mix)", bitrate=883)
        track02 = models.Audio.objects.create(title="Why Don't You Dance With Me (Radio Mix)", bitrate=846)
        track03 = models.Audio.objects.create(title="Why Don't You Dance With Me (Club Mix)", bitrate=848)
        track04 = models.Audio.objects.create(title="Why Don't You Dance With Me (Future Breeze's House Mix)", bitrate=852)
        track05 = models.Audio.objects.create(title="Why Don't You Dance With Me (Christian Linder Remix)", bitrate=684)

        page.content_set.add(description, info, track01, track02, track03, track04, track05)

    
    def test_pages(self,):
        url = f"{API_URL}/pages/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True,CELERY_TASK_EAGER_PROPOGATES=True)
    def test_page_detail(self,):
        url = f"{API_URL}/page/1/detail/?ordering_content=id"
        response = self.client.get(url)
        content_ids = map(lambda x: x["id"], response.json().get('content_set'))

        self.assertListEqual(list(content_ids), list(range(1, 8)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        time.sleep(60)
        response = self.client.get(url)
        data = response.json()
        for item in data.get("content_set"):
            self.assertEqual(item.get("view_count"), 1)

