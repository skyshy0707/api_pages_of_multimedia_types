from rest_framework import serializers

from . import models, tasks

class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Audio
        exclude = ('pages',)

class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Text
        exclude = ('pages',)

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Video
        exclude = ('pages',)


class ContentListSerializer(serializers.ListSerializer):

    def set_child(self, child):
        self.child = child

    def to_representation(self, data):
        ordering = self.context.get('request').query_params.getlist('ordering_content')
        iterable = data.all() if isinstance(data, models.models.Manager) else data

        serialized_data = []

        for item in iterable.order_by(*ordering):
            if isinstance(item, models.Audio):
                child = AudioSerializer()
            elif isinstance(item, models.Text):
                child = TextSerializer()
            elif isinstance(item, models.Video):
                child = VideoSerializer()
            else:
                raise TypeError(f"Некорректный экземпляр, класс {type(item)} не соотвествует данным")
            self.set_child(child)
            serialized_data.append(self.child.to_representation(item))
            tasks.plus_single_view.apply_async(args=(item.id,), countdown=20)
        return serialized_data

class ContentSerializer(serializers.ListSerializer):
    
    class Meta:
        list_serializer_class = ContentListSerializer

class PageSerializer(serializers.ModelSerializer):

    detail_url = serializers.CharField(source='get_detail_page')

    class Meta:
        model = models.Page
        fields = ('id', 'title', 'detail_url')

class PageDetailSerializer(serializers.ModelSerializer):

    content_set = serializers.SerializerMethodField('content_serializer')

    def content_serializer(self, page):
        context = { 'request': self.context.get('request') }
        content_set = models.Content.objects.filter(pages__in=[page]).select_subclasses().distinct()
        serializer = ContentSerializer(content_set, many=True, context=context, required=False, child=AudioSerializer())
        return serializer.data

    class Meta:
        model = models.Page
        fields = "__all__"