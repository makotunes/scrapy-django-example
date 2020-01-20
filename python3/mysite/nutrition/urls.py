from django.conf.urls import patterns, url
from nutrition import views
from django.views.generic import ListView
urlpatterns = [
    url(r'^nutrition/ITEM/$', views.AddCommentList.as_view()),
    url(r'^nutrition/ITEM/(?P<pk>[0-9]+)/$', views.AddCommentDetail.as_view()),
    url(r'^nutrition/item/$', views.ItemList.as_view()),
    url(r'^nutrition/item/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view()),
]
from django.views.generic.base import RedirectView


