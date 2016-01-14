import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.template import RequestContext
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string


def main_view(request):
	if request.method == 'POST':
		form_data = request.POST.dict()
		if form_data.get('form') == 'signin':
			if 'username' in form_data and 'password' in form_data and 'type' in form_data:
				user = authenticate(
					username=form_data.get('username', ''),
					password=form_data.get('password', '')
				)
				res = requests.post('%s%s' % (settings.DOMAIN, reverse('api:signin')), data=form_data)
				if res.ok:
					user = authenticate(
						username=form_data.get('username', ''),
						password=form_data.get('password', '')
					)
					login(request, user)
					return redirect(reverse('core:home'))
		elif form_data.get('form') == 'signup':
			form_data = request.POST.dict()
			res = requests.post('%s%s' % (settings.DOMAIN, reverse('api:signup')), data=form_data)
			if res.ok:
				if 'biller' in res.json() or 'user' in res.json():
					return render(
						request,
						'main.html',
						{'message': 'Ask admin to activate your account you are now registred with MyWallet'}
					)
				return render(
					request,
					'main.html',
					{'message': 'Kindly login to your account'}
				)
		return HttpResponse('Invalid data')
	return render(request, 'main.html', {})


@login_required(login_url='/mywallet')
def transaction_view(request):
	current_user = request.user
	context = {}
	res = requests.get('%s%s' % (settings.DOMAIN, reverse('api:transactions', args=[current_user.id])))
	context['txns'] = res.json()
	res = requests.get('%s%s' % (settings.DOMAIN, reverse('api:user', args=[current_user.id])))
	context['mywallet_user'] = res.json()
	return render(request, 'home.html', context)
