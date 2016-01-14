from django.contrib import admin
from django.conf.urls import url, include, patterns

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('core.urls', namespace='core')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/', include('api.urls', namespace='api')),
)