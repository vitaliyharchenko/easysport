from django.conf.urls import url

from .views import games_view, game_view, game_roster_view, game_invite_view, game_report_view, gameaction

urlpatterns = [
    url(r'^games$', games_view, name='games_view'),
    url(r'^game/(?P<game_id>\d+)$', game_view, name='game_view'),
    url(r'^roster/(?P<game_id>\d+)$', game_roster_view, name='game_roster_view'),
    url(r'^invite/(?P<game_id>\d+)$', game_invite_view, name='game_invite_view'),
    url(r'^report/(?P<game_id>\d+)$', game_report_view, name='game_report_view'),
    url(r'^game/action$', gameaction, name='gameaction'),
]