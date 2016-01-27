from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('pages.urls', namespace='pages')),


    url(r'^', include('pin_passcode.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
