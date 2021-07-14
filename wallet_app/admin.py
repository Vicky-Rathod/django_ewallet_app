from django.contrib import admin
from .models import Transaction,Type,TopUp,Wallet
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Type)
admin.site.register(TopUp)
admin.site.register(Wallet)