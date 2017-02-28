from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import login, logout, password_change

urlpatterns = [

    url(r'^$', views.dashboard),
    url(r'^data$', views.receive_data),
    url(r'^login/$', login,{'template_name': 'admin/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/login/'}, name = 'logout'),
    url(r'^change-password/$', password_change, {'post_change_redirect': '/dashboard/'}, name='password_change'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^view/(?P<id>\d+)/$', views.view_device, name='view'),

]