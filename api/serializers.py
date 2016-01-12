from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Biller, Customer, Transaction, Mywallet


class AdminSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
			'is_staff',
			'is_active',
			'is_superuser'
		)


class MywalletSerializer(serializers.HyperlinkedModelSerializer):
	user = AdminSerializer()

	class Meta:
		model = Mywallet
		fields = (
			'id',
			'user',
			'wallet',
			'contact_number',
		)


class BillerSerializer(serializers.HyperlinkedModelSerializer):
	biller = MywalletSerializer()

	class Meta:
		model = Biller
		fields = (
			'biller',
			'id',
			'unloaded_amount',
			'commission'
		)


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
	customer = MywalletSerializer()
	
	class Meta:
		model = Customer
		fields = ('customer', 'id')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	from_user = MywalletSerializer()
	to_user = MywalletSerializer()
	
	class Meta:
		model = Transaction
		fields = (
			'id',
			'from_user',
			'to_user',
			'amount',
			'note'
		)
