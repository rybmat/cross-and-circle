from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
import views

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, {'template_name': 'game/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/game'}, name='logout'),
    url(r'^password_change$', auth_views.password_change, {'template_name' : 'game/password_change.html'}, name='password_change'),
    url(r'^password_change_done$', auth_views.password_change_done, {'template_name' : 'game/message.html','extra_context':{'class':'info','title':'Pasword Changed!'}}, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name':'game/password_reset.html', 'extra_context':{'next':'password_reset_done','title':'Password reset', 'message':"Forgotten your password? Enter your email address below, and we'll email instructions for setting a new one."}}, name="password_reset"),
    url(r'^password_reset_done/$', auth_views.password_reset_done, {'template_name':'game/message.html','extra_context':{'class':'info', 'title':'Password reset successful!','message':"We've emailed you instructions for setting your password. You should be receiving them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder."}},name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name':'game/password_reset.html', 'extra_context':{'next':'password_reset_complete','title':'Enter new password', 'message':"Please enter your new password twice so we can verify you typed it in correctly."}}, name='password_reset_confirm'),
    url(r'^password_reset_complete/$', auth_views.password_reset_complete, {'template_name':'game/message.html', 'extra_context':{'class':'info','title':'Password reset complete!', 'message':'Now, you can log into your account.'}}, name='password_reset_complete'),
   
)
