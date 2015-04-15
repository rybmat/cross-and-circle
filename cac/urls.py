from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('cross_and_circle.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
