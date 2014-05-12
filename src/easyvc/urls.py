from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easyvc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'webapp.views.home', name='home'),
    url(r'^thankyou/$', 'webapp.views.thankyou', name='thankyou'),
    url(r'^VCSignup/$', 'webapp.views.VCSignup', name='VCSignup'),
    url(r'^StartupSignup/$', 'webapp.views.StartupSignup', name='StartupSignup'),
    url(r'^signin/$','webapp.views.signin',name='signin'),
    url(r'^VCUI/$','webapp.views.VCUI',name='VCUI'),
    url(r'^VCUpdate/$','webapp.views.VCUpdate',name='VCUpdate'),
    url(r'^startupUI/$','webapp.views.startupUI',name='startupUI'),
    url(r'^startupUpdate/$','webapp.views.startupUpdate',name='startupUpdate'),
    url(r'^signout/$','webapp.views.signout',name='signout'),
    url(r'^editVC/$','webapp.views.editVC',name='editVC'),
    url(r'^editStartup/$','webapp.views.editStartup',name='editStartup'),
    url(r'^VCEditUpdate/$','webapp.views.VCEditUpdate',name='VCEditUpdate'),
    url(r'^showVC/(?P<userName>\w+)$','webapp.views.showVC',name='showVC'),
    url(r'^showStartup/(?P<userName>\w+)$','webapp.views.showStartup',name='showStartup'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
