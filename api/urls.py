from django.conf.urls import patterns, url
from api import views
from django.views.generic import TemplateView


urlpatterns = patterns('',
	url(r'^signin', views.SignInView.as_view(), name='signin'),
	url(r'^signup', views.SignUpView.as_view(), name='signup'),
	# url(r'^logout', views.logout_view, name='logout'),
	# url(r'^home', views.home_view, name='home'),
	# url(r'^dashboard', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
	url(r'^edit-profile/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='edit_profile'),
	
	# # wallet admin urls
	url(r'^users', views.MywalletView.as_view(), name='users'),
	url(r'^user/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='user'),
	url(r'^activate-wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='activate_wallet_admin'),
	url(r'^deactivate-wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='deactivate_wallet_admin'),
	
	# # wallet biller urls
	url(r'^billers', views.BillerView.as_view(), name='billers'),
	url(r'^biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='biller'),
	url(r'^activate-biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='activate_biller'),
	url(r'^deactivate-biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='deactivate_biller'),

	# # wallet customer urls
	url(r'^customers', views.CustomerView.as_view(), name='customers'),
	url(r'^customer/(?P<user_id>[0-9]+)/$', views.CustomerView.as_view(), name='customer'),
	url(r'^deactivate-customer/(?P<user_id>[0-9]+)/$', views.CustomerView.as_view(), name='deactivate_customer'),

	# # wallet transaction urls
	url(r'^transactions/(?P<user_id>[0-9]+)/$', views.TransactionView.as_view(), name='transactions'),
	# url(r'^user-txn', views.user_txn, name='user_txn'),
)
