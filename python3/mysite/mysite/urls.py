from django.conf.urls import url, include
from django.contrib import admin
from nutrition import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index ),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    #url(r'^account/', include('allauth.urls')),
    #url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),

    url(r'^', include('nutrition.urls')),
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    ]

from rest_framework.authtoken import views

urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token),
    #url(r'^token-login/', TemplateView.as_view(template_name="token_login.html"), name='doc'),
]
from django.conf.urls import patterns
