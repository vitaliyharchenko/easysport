from django.conf.urls import url

from .views import games_view, game_view, game_edit_view, game_create_view, game_roster_view, game_invite_view, game_report_view, gameaction, game_email_invite, game_next_add

urlpatterns = [
    url(r'^games$', games_view, name='games_view'),
    url(r'^game/(?P<game_id>\d+)$', game_view, name='game_view'),
    url(r'^game/(?P<game_id>\d+)/edit$', game_edit_view, name='game_edit_view'),
    url(r'^game/create$', game_create_view, name='game_create_view'),
    url(r'^game/(?P<game_id>\d+)/add_next$', game_next_add, name='game_next_add'),
    url(r'^roster/(?P<game_id>\d+)$', game_roster_view, name='game_roster_view'),
    url(r'^invite/(?P<game_id>\d+)$', game_invite_view, name='game_invite_view'),
    url(r'^invite/sendemail/(?P<game_id>\d+)$', game_email_invite, name='game_email_invite'),
    url(r'^report/(?P<game_id>\d+)$', game_report_view, name='game_report_view'),
    url(r'^game/action$', gameaction, name='gameaction'),
]