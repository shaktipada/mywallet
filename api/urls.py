from django.conf.urls import patterns, url
from api import views


urlpatterns = patterns('',
	url(r'^signin', views.SignInView.as_view(), name='signin'),
	url(r'^signup', views.SignUpView.as_view(), name='signup'),
	url(r'^edit-profile/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='edit_profile'),
	url(r'^deactivate-account/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='deactivate_account'),
	
	# wallet admin urls
	url(r'^users', views.MywalletView.as_view(), name='users'),
	url(r'^user/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='user'),
	url(r'^activate-wallet-admin/(?P<user_id>[0-9]+)/$', views.MywalletView.as_view(), name='activate_wallet_admin'),
	
	# wallet biller urls
	url(r'^billers', views.BillerView.as_view(), name='billers'),
	url(r'^biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='biller'),
	url(r'^activate-biller/(?P<user_id>[0-9]+)/$', views.BillerView.as_view(), name='activate_biller'),

	# wallet customer urls
	url(r'^customers', views.CustomerView.as_view(), name='customers'),
	url(r'^customer/(?P<user_id>[0-9]+)/$', views.CustomerView.as_view(), name='customer'),

	# wallet transaction urls
	url(r'^transactions/(?P<user_id>[0-9]+)/$', views.TransactionView.as_view(), name='transactions'),
)
