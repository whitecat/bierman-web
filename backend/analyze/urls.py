from django.urls import path
from .views import analyze_file_view, analyze_url_view

urlpatterns = [
    path('url/', analyze_url_view, name='analyze_url_view'),
    path('file/', analyze_file_view, name='analyze_file_view'),
]
