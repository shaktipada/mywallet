from django.contrib import admin
from api.models import Mywallet, Biller, Customer, Transaction

admin.site.register(Mywallet)
admin.site.register(Biller)
admin.site.register(Customer)
admin.site.register(Transaction)
