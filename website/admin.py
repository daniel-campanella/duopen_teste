from django.contrib import admin
from .models import Account, Transaction, Merchant, CreditCardMetaData

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Merchant)
admin.site.register(CreditCardMetaData)
