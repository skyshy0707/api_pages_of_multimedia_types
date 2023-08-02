**Описание**

<br>

<<Скелет>> небольшого информационного сервиса метаданных мульмедийного контента.
Представлен API `страниц` как объектов с мульмедийным контентом.

<br>
<br>

**Возможности сервиса:**

<br>

Позволяет получать информцию о всех `страницах` с пагинацией и фильтрацией.

Позволяет получать подробную информацию о `странице`, на которой выложен контент следующих випов: аудио, видео, текст.

Со `страницей` может быть связан любой вид контента в любом количестве. Семантика такая: <<на `страницу` можно выложить любой вид контента в любом количестве>>. Например: на `странице` может быть 5 видео, 3 аудио и 7 текстов в любом порядке и в перемешку.

При обращении к API с деталями о `странице` счётчик просмотров каждого объекта контента, привязанного к `странице` увеличивается на единицу.

<br>
<br>

**Настройки проекта:**

<br>

- Переменные окружения: ./src/.env

  Здесь необходимо определить:

    - `BASE_URL` - базовый адрес лок. сервера - в соответствии с запуском проекта (номер порта для запуска определён в последней строке скрипта `./runserver-entrypoint.sh`),

    - `TZ` - часовой пояс

  - Настройки базы данных:

      - `POSTGRES_HOST`=db
      - `POSTGRES_PORT`=5432
      - `POSTGRES_DB`
      - `POSTGRES_USER`
      - `POSTGRES_PASSWORD`
      - `POSTGRES_HOST_AUTH_METHOD`=trust
      - `PGDATA`=/var/lib/postgres/data`

  - Параметры суперпользователя:

      - `DJANGO_SUPERUSER_USERNAME`,
      - `DJANGO_SUPERUSER_PASSWORD`,
      - `DJANGO_SUPERUSER_EMAIL`

  - Точки входа (sh-скрипты):

    - Точка входа в runserver процесс: ./runserver-entrypoint.sh:

      - Параметры для команды создания суперпользователя createsuperuser_from_settings определены в файле .env -- см. выше.

    - Точка входа для worker: ./worker-entrypoint.sh

    - Точка входа для запуска автотестов: ./autotests.sh

<br>
<br>

**Описание конечных точек с примерами вызовов:**

<br>

Url API: **_<BASE_URL>/api_**

<br>

1. $\color[RGB]{0,0,0}{\textsf{Получить список страниц:}}$ **_/pages_**

<br>

  $\color[RGB]{153,0,153}{\textsf{Methods:}}$ $\color[RGB]{0,204,0}{\textsf{GET}}$

  $\color[RGB]{153,0,153}{\textsf{Params:}}$ ```{ 'search': 'Значение поисковой фильтрации страниц по атрибуту title', 'page': <Номер страницы> }```

  $\color[RGB]{153,0,153}{\textsf{Response:}}$ ```json { "count": <Число объектов в results>, "next": '<Url следующей страницы>', "previous": '<Url предыдущей страницы>', "results": <Список страниц в виде json-данных[ { "id": <id страницы>, "title": "<Заголовок/Название страницы>", "detail_url": "<Url конечной точки с детальной информацией о странице>" }, ... ]> }```

  $\color[RGB]{255,128,0}{\textsf{Example:}}$

  $\color[RGB]{0,204,0}{\textsf{GET}}$ $\color[RGB]{0,0,255}{\textsf{/pages}}$

  ```json { "count": 6, "next": "http://127.0.0.1:8000/api/pages/?page=2", "previous": null, "results":[ { "id": 1, "title": "Города России","detail_url" :"http://127.0.0.1:8000/api/page/1/detail" }, { "id": 2, "title": "Future Breeze - Why Don't You Dance With Me? [1996]","detail_url": "http://127.0.0.1:8000/api/page/2/detail" }, { "id": 3, "title": "Раздел Youtube-ролики", "detail_url": "http://127.0.0.1:8000/api/page/3/detail" }, { "id": 4, "title": "Electronic", "detail_url": "http://127.0.0.1:8000/api/page/4/detail" }, { "id": 5, "title": "Dance","detail_url": "http://127.0.0.1:8000/api/page/5/detail" } ] }```

<br>

2. $\color[RGB]{0,0,0}{\textsf{Получить детальную информацию о странице:}}$ **_/page/\<id>\/detail_**

<br>

  $\color[RGB]{153,0,153}{\textsf{Methods:}}$ $\color[RGB]{0,204,0}{\textsf{GET}}$

  $\color[RGB]{153,0,153}{\textsf{Params:}}$ ```{ "ordering_content": <Набор атрибутов для сортировки объектов контента, привязанного к странице[ 'attr1/-attr1', ... ]>, }```

  где `attr1` -- сортировка по атрибуту `attr1` в порядке возврастания, `-attr1` -- сорптировка по атрибуту `attr1` в порядке убывания

  $\color[RGB]{153,0,153}{\textsf{Response:}}$ ```json { "id": <id страницы>, "content_set": <Список объектов, приваязанных к странице[ { "id": <id контента>, "title": "Название", "view_count": <Число просмотров>, "bitrate": <Количество бит в секунду -- только для контента вида аудио>, "file_link": "<Url на видео-файл> -- только для контента вида видео", "subtitles_link": "<Url на файл субтитров> -- только для контента вида видео", "content": "<Текстовое содержимое> -- только для контента вида текст" }, ... ]>, "title": "<Заголовок/Название страницы>" }```

  $\color[RGB]{255,128,0}{\textsf{Example:}}$

  $\color[RGB]{0,204,0}{\textsf{GET}}$ $\color[RGB]{0,0,255}{\textsf{/page/1/detail}}$

  ```json { "id": 1, "content_set": [ { "id": 1, "title": "Омск", "view_count": 42, "file_link": "https://www.youtube.com/watch?v=WHPu5tmFKZQ", "subtitles_link": null }, { "id": 2,"title": "Уфа", "view_count": 42, "file_link": "https://www.youtube.com/watch?v=KAnpPaF_gx0", "subtitles_link": null }, { "id": 3, "title": "Описание", "view_count": 42, "content": "Обзор городов России от первого лица." } ], "title": "Города России" }```

<br>
<br>

**Запуск проекта:**

- Сборка:

```
docker-compose up --build
```

- Автотесты:

```
docker-compose up autotests
```

- Запуск сервера:

```
docker-compose up runserver
```