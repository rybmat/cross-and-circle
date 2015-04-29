from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^rest/', include('cross_and_circle.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #url(r'^admin/', include(admin.site.urls)),
)
