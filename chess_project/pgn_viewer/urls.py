from django.urls import path
from django.conf.urls.static import static  # Add this import
from . import views
from . import load
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path('load_pgn/', views.load_pgn, name='load_pgn'),
    path('get_games_list/', load.get_games_list, name='get_games_list'),
    path('load_specific_game/', load.load_specific_game, name='load_specific_game'),
    path('get_related_games/', load.get_related_games, name='get_related_games'),
    path('upload/', views.upload_pgn, name='upload_pgn'),
]

# Only add static URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)