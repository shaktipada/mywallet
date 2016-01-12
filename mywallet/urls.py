from django.contrib import admin
from django.conf.urls import url, include, patterns
from rest_framework import routers
from django.views.generic import TemplateView

from api import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# urlpatterns = [
    # url(r'^', include(router.urls)),
# ]


admin.autodiscover()

urlpatterns = patterns('',
	url(r'^main', TemplateView.as_view(template_name='main.html'), name='main'),
	url(r'^signin', views.SignInView.as_view(), name='signin'),
	url(r'^signup', views.SignUpView.as_view(), name='signup'),
	url(r'^logout', views.logout_view, name='logout'),
	url(r'^dashboard-home', views.home_view, name='dashboard_home'),
	url(r'^dashboard', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
	
	# wallet admin urls
	url(r'^wallet-admins', views.MywalletView.as_view(), name='wallet_admins'),
	url(r'^wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='wallet_admin'),
	url(r'^activate-wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='activate_wallet_admin'),
	url(r'^deactivate-wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='deactivate_wallet_admin'),
	url(r'^edit-wallet-admin', views.MywalletView.as_view(), name='edit_wallet_admin'),
	
	# wallet biller urls
	url(r'^billers', views.BillerView.as_view(), name='billers'),
	url(r'^biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='biller'),
	url(r'^activate-biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='activate_biller'),
	url(r'^deactivate-biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='deactivate_biller'),
	url(r'^edit-biller', views.BillerView.as_view(), name='edit_biller'),

	# wallet customer urls
	url(r'^customers', views.CustomerView.as_view(), name='customers'),
	url(r'^customer/(?P<user_id>[0-9]+)/$', views.CustomerView.as_view(), name='customer'),
	url(r'^deactivate-customer/(?P<user_id>[0-9]+)/$', views.CustomerView.as_view(), name='deactivate_customer'),
	url(r'^edit-customer', views.CustomerView.as_view(), name='edit_customer'),

	# wallet transaction urls
	url(r'^transactions', views.TransactionView.as_view(), name='transactions'),
	url(r'^transact', views.TransactionView.as_view(), name='transact'),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)