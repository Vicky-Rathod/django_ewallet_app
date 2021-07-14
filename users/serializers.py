from wallet_app.models import Wallet
from rest_framework import serializers
from .models import *
from .helper import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email' , 'password' ,'phone']

    def create(self , validated_data):
        user = User.objects.create(email = validated_data['email'] , phone= validated_data['phone'])
        user.set_password(validated_data['password'])
        Wallet.objects.create(user=user)
        user.save()
        send_otp_to_mobile(user.phone , user)
        return user