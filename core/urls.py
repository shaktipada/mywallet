from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from core import views

urlpatterns = patterns('',
	url(r'^mywallet$', views.main_view, name='main'),
	url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/mywallet'}, name='logout'),
	url(r'^home$', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
	url(r'^transaction$', views.transaction_view, name='txn'),
	url(r'^billers$', views.billers_view, name='billers'),
	url(r'^customers$', views.customers_view, name='customers'),
	url(r'^users$', views.users_view, name='users'),
)
