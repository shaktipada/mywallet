import json
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Biller, Customer, Transaction, Mywallet
from api.serializers import BillerSerializer, CustomerSerializer, TransactionSerializer, \
	MywalletSerializer


class SignInView(APIView):

	def post(self, request):
		print '------'
		form_data = request.data.dict()
		print form_data
		user = None
		if 'type' not in form_data:
			return Response(
				data=json.dumps({'error': 'Login type not specified'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		elif form_data.get('type') not in ['admin', 'biller', 'customer']:
			return Response(
				data=json.dumps({'error': 'Login type inappropriate'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		try:
			user = Mywallet.objects.filter(
				(
					Q(user__email=form_data.get('username', '')) |
					Q(user__username=form_data.get('username', '')) |
					Q(contact_number=form_data.get('username', ''))
				),
				user__is_active=True,
				user__is_staff=True if form_data.get('type') == u'admin' else False,
			).first()
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)
		if user is not None:
			user = authenticate(username=user.user.username, password=form_data.get('password', ''))
			print "########", user
			if user is not None:
				print "########", user
				login(self.request, user)
				mywallet_user = Mywallet.objects.get(user=user)
				print "::::::::", mywallet_user
				if form_data.get('type') == 'admin':
					serializer = MywalletSerializer(mywallet_user)
				elif form_data.get('type') == 'biller':
					print "biller"
					serializer = BillerSerializer(
						Biller.objects.get(biller__user__id=mywallet_user.user.id)
					)
					print "billerLLLL"
				elif form_data.get('type') == 'customer':
					serializer = CustomerSerializer(
						Customer.objects.get(customer__user__id=mywallet_user.user.id)
					)
				request.session['data'] = serializer.data
				print "??????????", request.session['data']
				return Response(serializer.data)
		return Response(
			data=json.dumps({'error': 'Unauthorized'}),
			status=status.HTTP_404_UNAUTHORIZED
		)


class SignUpView(APIView):

	def post(self, request, format=None):
		form_data = request.data.dict()
		print form_data
		user = None
		if 'type' not in form_data:
			return Response(
				data=json.dumps({'error': 'Login type not specified'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		elif form_data.get('type') not in ['admin', 'biller', 'customer']:
			return Response(
				data=json.dumps({'error': 'Login type inappropriate'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		try:
			user = Mywallet.objects.filter(
				(
					Q(user__email=form_data.get('email', '')) |
					Q(user__username=form_data.get('username', '')) |
					Q(contact_number=form_data.get('contact_number', ''))
				),
				user__is_active=True,
				user__is_staff=True if form_data.get('type') is 'admin' else False,
			).first()
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)
		if user is None:
			print ">>>>>>", user
			user = User.objects.create_user(
				form_data.get('username', ''),
				email=form_data.get('email', ''),
				password=form_data.get('password', ''),
				**{
					'first_name': form_data.get('first-name', ''),
					'last_name': form_data.get('last-name', ''),
				}
			)
			if form_data.get('type') == 'biller':
				user.is_active = False
				user.save()
			mywallet_user = Mywallet.objects.create(
				user=user,
				contact_number=form_data.get('contact_number')
			)
			if form_data.get('type') == 'admin':
				serializer = MywalletSerializer(mywallet_user)
			elif form_data.get('type') == 'biller':
				serializer = BillerSerializer(
					Biller.objects.create(biller=mywallet_user)
				)
			elif form_data.get('type') == 'customer':
				serializer = CustomerSerializer(
					Customer.objects.create(customer=mywallet_user)
				)
			return Response(serializer.data)
		Response(
			data=json.dumps({'error': 'Username / EmailID already in use'}),
			status=status.HTTP_400_BAD_REQUEST
		)


class MywalletView(APIView):

	def get_object(self, user_id=None):
		try:
			if user_id is None:
				return Mywallet.objects.all()
			else:
				return Mywallet.objects.get(user__id=user_id)
		except Exception, e:
			raise Http404
			
	def get(self, request, user_id=None):
		mywallet_user = None
		try:
			if user_id is None:
				mywallet_user = self.get_object()
			else:
				mywallet_user = self.get_object(user_id)
			if mywallet_user is not None:
				serializer = MywalletSerializer(
					mywallet_user,
					many=True if isinstance(mywallet_user, QuerySet) else False
				)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'Please contact superuser to activate your account'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		except Exception as e:
			return Response(
				data=json.dumps({'error': 'Unauthorized'}),
				status=status.HTTP_404_UNAUTHORIZED
			)
	
	def post(self, request, user_id):
		current_user = request.user
		try:
			if current_user.is_superuser:
				mywallet_user = self.get_object(user_id)
				mywallet_user.user.is_staff = True
				mywallet_user.save()
				serializer = MywalletSerializer(mywallet_user)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'Unauthorized'}),
				status=status.HTTP_404_UNAUTHORIZED
			)
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)

	def put(self, request):
		current_user = request.user
		form_data = request.data
		mywallet_user = None
		try:
			mywallet_user = self.get_object(current_user.id)
			if mywallet_user is not None and mywallet_user.is_staff:
				if 'password' in form_data:
					mywallet_user.user.password = make_password(form_data.get('password', ''))
				mywallet_user.user.first_name = form_data.get('first-name', '')
				mywallet_user.user.last_name = form_data.get('last-name', ''),
				mywallet_user.contact_number = form_data.get('contact_number', '')
				mywallet_user.save()
				serializer = MywalletSerializer(mywallet_user)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'User Not found'}),
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)

	def delete(self, request, user_id):
		try:
			current_user = request.user
			if current_user.is_superuser:
				mywallet_user = None
				mywallet_user = self.get_object(user_id)
				if mywallet_user is not None:
					mywallet_user.user.is_active = False
					mywallet_user.user.is_staff = False
					mywallet_user.save()
					return Response(status=status.HTTP_204_NO_CONTENT)
				return Response(
					data=json.dumps({'error': 'User Not found'}),
					status=status.HTTP_404_NOT_FOUND
				)
			return Response(
				data=json.dumps({'error': 'Unauthorized'}),
				status=status.HTTP_404_UNAUTHORIZED
			)
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)


class BillerView(APIView):

	def get_object(self, user_id=None):
		try:
			if user_id is None:
				return Biller.objects.all()
			else:
				return Biller.objects.get(biller__user__id=user_id)
		except Exception, e:
			raise Http404
			
	def get(self, request, user_id=None):
		biller = None
		print "+++++++++++"
		try:
			if user_id is None:
				biller = self.get_object()
			else:
				biller = self.get_object(user_id)
			if biller is not None:
				print "MMMMMMMMMMMMM", biller
				serializer = BillerSerializer(
					biller,
					many=True if isinstance(biller, QuerySet) else False
				)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'Please contact MyWallet to activate your account'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		except Exception as e:
			return Response(
				data=json.dumps({'error': 'Unauthorized'}),
				status=status.HTTP_404_UNAUTHORIZED
			)
	
	def post(self, request, user_id):
		current_user = request.user
		if current_user.is_staff:
			try:
				biller = self.get_object(user_id)
				biller.biller.user.is_active = True
				biller.commission = float(request.data.get('commission', 0.0)) / 100.0
				biller.save()
				serializer = BillerSerializer(biller)
				return Response(serializer.data)
			except Exception as e:
				Response(
					data=json.dumps({'error': 'DB error'}),
					status=status.HTTP_404_NOT_FOUND
				)
		return Response(
			data=json.dumps({'error': 'Unauthorized'}),
			status=status.HTTP_404_UNAUTHORIZED
		)

	def put(self, request):
		form_data = request.data
		current_user = request.user
		biller = None
		try:
			biller = self.get_object(current_user.id)
			if biller is not None:
				if 'password' in form_data:
					biller.biller.user.password = make_password(form_data.get('password'))
				biller.biller.user.first_name = form_data.get('first_name', '')
				biller.biller.user.last_name = form_data.get('last_name', '')
				biller.biller.contact_number = form_data.get('contact_number', '')
				biller.save()
				serializer = BillerSerializer(biller)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'User Not found'}),
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)

	def delete(self, request, user_id):
		current_user = request.user
		if current_user.is_staff:
			biller = None
			biller = self.get_object(user_id)
			if biller is not None:
				biller.biller.user.is_active = False
				biller.save()
				return Response(status=status.HTTP_204_NO_CONTENT)
			return Response(
				data=json.dumps({'error': 'User Not found'}),
				status=status.HTTP_404_NOT_FOUND
			)
		return Response(
			data=json.dumps({'error': 'Unauthorized'}),
			status=status.HTTP_404_UNAUTHORIZED
		)


class CustomerView(APIView):

	def get_object(self, user_id=None):
		try:
			if user_id is None:
				return Customer.objects.all()
			else:
				return Customer.objects.get(customer__user__id=user_id)
		except Exception, e:
			raise Http404
			
	def get(self, request, user_id=None):
		customer = None
		try:
			if user_id is None:
				customer = self.get_object()
			else:
				customer = self.get_object(user_id)
			if customer is not None:
				serializer = CustomerSerializer(
					customer,
					many=True if isinstance(customer, QuerySet) else False
				)
				return Response(serializer.data)
			return Response(status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(
				data=json.dumps({'error': 'Unauthorized'}),
				status=status.HTTP_404_UNAUTHORIZED
			)

	def put(self, request):
		form_data = request.data
		current_user = request.user
		customer = None
		try:
			customer = self.get_object(current_user.id)
			if customer is not None:
				if 'password' in form_data:
					customer.customer.user.password = make_password(form_data.get('password'))
				customer.customer.user.first_name = form_data.get('first-name', '')
				customer.customer.user.last_name = form_data.get('last-name', '')
				customer.customer.contact_number = form_data.get('contact_number', '')
				customer.save()
				serializer = CustomerSerializer(customer)
				return Response(serializer.data)
			return Response(
				data=json.dumps({'error': 'User Not found'}),
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			Response(
				data=json.dumps({'error': 'DB error'}),
				status=status.HTTP_404_NOT_FOUND
			)

	def delete(self, request):
		current_user = request.user
		customer = self.get_object(current_user.id)
		if customer is not None:
			customer.customer.user.is_active = False
			customer.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(
			data=json.dumps({'error': 'User Not found'}),
			status=status.HTTP_404_NOT_FOUND
		)


class TransactionView(APIView):
	
	def check_admin(self, user_id):
		user = None
		try:
			user = Mywallet.objects.get(user__id=user_id, user__is_active=True, user__is_staff=True)
			return user
		except Exception as e:
			raise Http404

	def check_biller(self, user_id):
		biller = None
		try:
			biller = Biller.objects.get(biller__user__id=user_id, biller__user__is_active=True)
			return biller
		except Exception as e:
			raise Http404

	def check_customer(self, user_id):
		customer = None
		try:
			customer = Customer.objects.get(customer__user__id=user_id, customer__user__is_active=True)
			return customer
		except Exception as e:
			raise Http404

	def get(self, request):
		current_user = request.user
		user = self.check_admin(current_user.id)
		txn = None
		if user is not None:
			txn = Transaction.objects.all()
		else:
			txn = Transaction.objects.filter(
				(
					Q(from_user__user=current_user, to_user__user=current_user) |
					Q(to_user__user=current_user) |
					Q(from_user__user=current_user)
				)
			)
		if txn is not None:
			serializer = TransactionSerializer(txn)
			return Response(serializer.data)
		return Response(
			data=json.dumps({'error': 'User Not found'}),
			status=status.HTTP_404_NOT_FOUND
		)

	def post(self, request):
		current_user = request.user
		form_data = request.data
		if 'type' not in form_data:
			return Response(
				data=json.dumps({'error': 'Transaction type not specified'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		elif form_data.get('type') != 'unload' or form_data.get('type') != 'transfer' or\
			form_data.get('type') != 'load' or form_data.get('type') != 'pay':
			return Response(
				data=json.dumps({'error': 'Transaction type inappropriate'}),
				status=status.HTTP_400_BAD_REQUEST
			)
		if form_data('type') == 'unload':
			biller = self.check_biller(current_user.id)
			if biller is not None and biller.biller.wallet > 0:
				biller.biller.wallet -= float(form_data.get('amount', 0.0))
				commission = biller.commission * float(form_data.get('amount', 0.0))
				biller.unloaded_amount += float(form_data.get('amount', 0.0)) - commission
				mywallet_user = Mywallet.objects.get(user__id=current_user.id)
				mywallet = Mywallet.objects.filter(user__is_superuser=True).first()
				mywallet.wallet += commission
				biller.save()
				mywallet.save()
				txn = Transaction.objects.create(
					from_user=mywallet_user,
					to_user=mywallet_user,
					amount=float(form_data.get('amount', 0.0)),
					note=form_data.get('note', '')
				)
				serializer = TransactionSerializer(txn)
				return Response(serializer.data)
		elif form_data('type') == 'transfer':
			from_customer = self.check_customer(current_user.id)
			if from_customer.check_password(form_data.get('password')):
				to_customer = self.check_customer(int(form_data('to_id')))
				if to_customer is not None and from_customer is not None and from_customer.customer.wallet > 0:
					from_customer.customer.wallet -= float(form_data.get('amount', 0))
					commission = .01 * float(form_data.get('amount', 0))
					to_customer.customer.wallet += float(form_data.get('amount', 0)) - commission
					to_customer.save()
					from_customer.save()
					mywallet = Mywallet.objects.filter(user__is_superuser=True).first()
					mywallet.wallet += commission
					mywallet.save()
					txn = Transaction.objects.create(
						from_user=Mywallet.objects.get(user__id=current_user.id),
						to_user=Mywallet.objects.get(user__id=int(form_data.get('to_id'))),
						amount=float(form_data.get('amount', 0)),
						note=form_data.get('note', '')
					)
					serializer = TransactionSerializer(txn)
					return Response(serializer.data)
		elif form_data('type') == 'pay':
			customer = self.check_customer(current_user.id)
			biller = self.check_biller(int(form_data.get('biller_id')))
			if customer is not None and customer.customer.wallet > 0:
				customer.customer.wallet -= float(form_data.get('amount', 0.0))
				biller.biller.wallet += float(form_data.get('amount', 0))
				customer.save()
				biller.save()
				txn = Transaction.objects.create(
					from_user=Mywallet.objects.get(user__id=customer.customer.user.id),
					to_user=Mywallet.objects.get(user__id=biller.biller.user.id),
					amount=float(form_data.get('amount', 0)),
					note=form_data.get('note', '')
				)
				serializer = TransactionSerializer(txn)
				return Response(serializer.data)
		if form_data('type') == 'load':
			customer = self.check_customer(current_user.id)
			if customer is not None:
				customer.customer.wallet += float(form_data.get('amount', 0.0))
				customer.save()
				mywallet_user = Mywallet.objects.get(user__id=current_user.id)
				txn = Transaction.objects.create(
					from_user=mywallet_user,
					to_user=mywallet_user,
					amount=float(form_data.get('amount', 0.0)),
					note=form_data.get('note', '')
				)
				serializer = TransactionSerializer(txn)
				return Response(serializer.data)
		return Response(
			data=json.dumps({'error': 'Unauthorized'}),
			status=status.HTTP_404_UNAUTHORIZED
		)


# def logout_view(request):
# 	session_data = request.session['data']
# 	print ">>>>>>>>", session_data
# 	del request.session['data']
# 	if 'user' in session_data:
# 		res = redirect(reverse('dashboard'))
# 	elif 'biller' in session_data or 'customer' in session_data:
# 		res = redirect(reverse('main'))
# 	logout(request)
# 	return res

def logout_view(request):
	print ">>>>>>>>>>", request.session['data']
	del request.session['data']
	request.session.flush()
	logout(request)
	return redirect(reverse('main'))


@login_required
def home_view(request):
	session_data = request.session['data']
	context = {}
	if 'user' in session_data:
		if session_data.get('user').get('is_superuser'):
			context['message'] = 'Welcome MyWallet superuser %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
		else:
			context['message'] = 'Welcome MyWallet staff %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
	elif 'biller' in session_data:
		if session_data.get('user').get('is_superuser'):
			context['message'] = 'Welcome MyWallet superuser %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
		else:
			context['message'] = 'Welcome MyWallet staff %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
	elif 'customer' in session_data:
		if session_data.get('user').get('is_superuser'):
			context['message'] = 'Welcome MyWallet superuser %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
		else:
			context['message'] = 'Welcome MyWallet staff %s ' % \
				session_data.get('user').get('first_name') + " " + session_data.get('user').get('last_name')
	return render(request, 'home.html', context)
