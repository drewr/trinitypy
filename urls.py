from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = []

for dirname in ('css', 'js', 'img'):
    urlpatterns += patterns('',
        ('^' + dirname + '/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': "%s/static/%s/" % (settings.HOME, dirname),
          'show_indexes': True}))

## urlpatterns += patterns('django.views.generic.simple',
##     (r'^(?P<path>.*)\.html$', 'redirect_to', {'url': '/%(path)s/'}),
## )

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', include(admin.site.urls)),
    (r'^cm/', include('cm.urls')),
    (r'^audio.xml$', 'django.views.generic.simple.direct_to_template',
            dict(template='audio.xml',
                 mimetype='application/xml',
                 extra_context={})),
    (r'^$', 'django.views.generic.simple.direct_to_template',
            dict(template='index.html')),
)

