from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^tenant_info', hello.views.get_tenant, name='get_tenant'),
    url(r'^thanks', hello.views.thanks, name='thanks'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls))

)
