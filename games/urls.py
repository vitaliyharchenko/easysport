from django.conf.urls import url

from .views import games_view, game_view, gameaction

urlpatterns = [
    url(r'^games$', games_view, name='games_view'),
    url(r'^game/(?P<game_id>\d+)$', game_view, name='game_view'),
    url(r'^game/action$', gameaction, name='gameaction'),
]