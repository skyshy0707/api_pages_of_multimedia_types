from rest_framework import generics, filters

from . import models, serializers

# Create your views here.

class PagesListView(generics.ListAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    
class PageDetailView(generics.RetrieveAPIView):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageDetailSerializer