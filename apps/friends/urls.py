from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^add_friend/(?P<friend_id>\d+)$', views.add_friend, name='add_friend'),

    url(r'^remove_friend/(?P<friend_id>\d+)$', views.remove_friend, name='remove_friend'),
    
]
