from django.db import models
from django.contrib.auth.models import User


class DateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Mywallet(DateTimeBase):
	user = models.OneToOneField(User)
	wallet = models.FloatField(default=0.0)
	contact_number = models.CharField(max_length=15)

	def __unicode__(self):
		return u"%s" % self.user.username


class Biller(DateTimeBase):
	biller = models.ForeignKey(Mywallet)
	unloaded_amount = models.FloatField(default=0.0)
	commission = models.FloatField(default=0.0)

	@classmethod
	def confirm(cls, user_id):
		try:
			Biller.objects.get(biller__user__id=user_id, biller__user__is_active=True)
			result = True
		except Biller.DoesNotExist:
			result = False
		return result

	def __str__(self):
		return u'%s' % self.biller.user.username


class Customer(DateTimeBase):
	customer = models.ForeignKey(Mywallet)

	@classmethod
	def confirm(cls, user_id):
		try:
			Customer.objects.get(customer__user__id=user_id, customer__user__is_active=True)
			result = True
		except Customer.DoesNotExist:
			result = False
		return result

	def __str__(self):
		return u'%s' % self.customer.user.username


class Transaction(DateTimeBase):
	from_user = models.ForeignKey(Mywallet, related_name='txn_from')
	to_user = models.ForeignKey(Mywallet, related_name='txn_towards')
	amount = models.FloatField(default=0.0)
	note = models.CharField(max_length=150, null=True, blank=True)
	
	def __unicode__(self):
		return u'%s' % self.from_user.user.username
