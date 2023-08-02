from django.urls import path

from . import views

urlpatterns = [
    path('pages/', views.PagesListView.as_view()),
    path('page/<int:pk>/detail/', views.PageDetailView.as_view()),
]