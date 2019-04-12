from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url
app_name = 'time_manage'   #影响登陆
urlpatterns = [
    path('', views.home_page, name='home'),
    path('calendar',views.CalendarView.as_view(), name='calendar'),
    url(r'^index/$', views.index, name='index'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
]