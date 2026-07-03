from django.urls import path
from . import views  

urlpatterns = [
    # 1. Serves the visual dashboard HTML layout at http://127.0.0.1:8000/
    path('', views.dashboard_view, name='system_dashboard'), 
    
    # 2. Serves the background JSON streams at http://127.0.0.1:8000/api/feed/
    path('api/feed/', views.feed_endpoint, name='live_tech_feed'), 
]