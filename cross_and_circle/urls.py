from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    url(r'^token/$', views.Token.as_view(), name='token'),

    url(r'^players/$', views.Players.as_view(), name='users'),
    url(r'^players/(?P<username>[A-Za-z_0-9]+)/$', views.PlayerDetails.as_view(), name='user-detail'),
    url(r'^players/(?P<username>[A-Za-z_0-9]+)/stats/$', views.PlayerStats.as_view(), name='user-stats'),
    url(r'^players/(?P<username>[A-Za-z_0-9]+)/games/$', views.PlayerGames.as_view(), name='user-games'),

    url(r'^games/$', views.Games.as_view(), name='games'),
    url(r'^games/(?P<pk>[0-9]+)/$', views.GameDetails.as_view(), name='game-detail'),
    url(r'^games/(?P<pk>[0-9]+)/moves/$', views.Moves.as_view(), name='game-moves'),

    url(r'^requests/$', views.Requests.as_view(), name='gamerequests'),
    url(r'^requests/(?P<pk>[0-9]+)/$', views.RequestDetails.as_view(), name='gamerequest-detail'),

    url(r'^accepted-requests/', views.Accepted.as_view(), name='accepted-requests'),
)

urlpatterns = format_suffix_patterns(urlpatterns)