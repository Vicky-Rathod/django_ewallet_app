from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import *

class TypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Type
        feilds = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance','user']
class TransactionSeializer(serializers.ModelSerializer):
    debited_wallet = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    class Meta : 
        model = Transaction
        fields = ['credited_to','debited_wallet','amount']
class TopUpSeializer(serializers.ModelSerializer):
    class  Meta : 
        model = TopUp
        fields = ['wallet','amount','description']