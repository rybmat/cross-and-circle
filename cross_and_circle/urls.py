from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^players/$', views.Players.as_view()),
    url(r'^players/(?P<player_name>[A-Za-z_]+)/$', views.PlayerDetails.as_view()),
    url(r'^players/(?P<player_name>[A-Za-z_]+)/stats/$', views.PlayerStats.as_view()),
    url(r'^players/(?P<player_name>[A-Za-z_]+)/games/$', views.PlayerGames.as_view()),

    url(r'^games/$', views.Games.as_view()),
    url(r'^games/(?P<id>[0-9]+)/$', views.GameDetails.as_view()),
    url(r'^games/(?P<id>[0-9]+)/board/$', views.GameBoard.as_view()),

    url(r'^requests/$', views.Requests.as_view()),
    url(r'^requests/(?P<player_name>[A-Za-z_]+)/$', views.RequestPerPlayer.as_view()),
    url(r'^requests/(?P<id>[0-9]+)/$', views.RequestDetails.as_view()),


)

urlpatterns = format_suffix_patterns(urlpatterns)