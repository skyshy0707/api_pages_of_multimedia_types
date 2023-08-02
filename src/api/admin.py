from django.contrib import admin

# Register your models here.
from . import models

class ContentInline(admin.TabularInline):
    model = models.Content.pages.through

class PageAdmin(admin.ModelAdmin):
    inlines = (ContentInline,)
    list_display = ('title',)

class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'bitrate')

class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'content')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'file_link', 'subtitles_link')

admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Audio, AudioAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Video, VideoAdmin)