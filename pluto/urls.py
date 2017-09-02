# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 01.07.2017
from django.conf.urls import url

from pluto import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test', views.test),
    url(r'^signup', views.signup),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^me', views.me),
    url(r'^profile/(?P<profile_id>[0-9]+)', views.profile),
    url(r'^mate_it/(?P<profile_id>[0-9]+)', views.mate_it),
    url(r'^mates', views.mates),
    url(r'^settings', views.settings),

    url(r'^level/(?P<level_id>[0-9]+)/play', views.play),

    url(r'^levels', views.levels),
    url(r'^level/(?P<level_id>[0-9]+)', views.level),

    url(r'^play/(?P<level_id>[0-9]+)', views.play),

    url(r'^records', views.record),
    url(r'^record/level=(?P<level_id>[0-9]+)&user=(?P<by_id>[0-9]+)', views.record),
    url(r'^record/level=(?P<level_id>[0-9]+)', views.record),
    url(r'^record/user=(?P<by_id>[0-9]+)', views.record),

    url(r'^creator/(?P<level_id>[0-9]+)', views.creator),
    url(r'^creator/', views.creator)
]
