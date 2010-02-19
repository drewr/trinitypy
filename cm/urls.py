from django.conf.urls.defaults import *

urlpatterns = patterns("cm.views",
    (r"^subscribe/$", "subscribe"),
    (r"^$", "index"),
)
