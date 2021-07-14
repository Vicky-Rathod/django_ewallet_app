from abc import ABCMeta
from django.core.checks.messages import Error
from django.db.models import base
from django.shortcuts import render
from .models import *
from .serializers import *
import razorpay
import requests
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.




class CreateTypeViewset(viewsets.ModelViewSet):

    serializer_class = TypeSerializer
    queryset = Type.objects.all()

class CreateWalletViewset(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()


#Handles Credit and Debit Amount from the Model
 
def transaction(cred_t,user,amount):
    credited_to = Wallet.objects.get(id = int(cred_t))
    debited_w = Wallet.objects.get(user=user)
    print(credited_to.balance)
    print(amount)
    print(debited_w.balance)
    try :
        if debited_w.balance >= int(amount):
            Wallet.objects.filter(id = int(cred_t)).update(balance = int(credited_to.balance) + int(amount) )
            Wallet.objects.filter(user=user).update(balance = int(debited_w.balance) - int(amount) )
    except:
        return Response({"Response": "Insufficient Balance "})
    return Wallet.objects.get(id = int(cred_t))
class CreateTransactionViewset(viewsets.ModelViewSet):
    serializer_class = TransactionSeializer
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    def perform_create(self,serializers):
        debited_wallet = Wallet.objects.get(user = self.request.user )
        user = self.request.user
        credited_to = transaction(self.request.data['credited_to'],user,self.request.data['amount'])
        Transaction.objects.create(credited_to = credited_to,debited_wallet = debited_wallet, amount = int(self.request.data['amount']))
        return Response({"Payment":"Success"})
        

class  CreateTopUpViewset(viewsets.ModelViewSet):
    queryset = TopUp.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TopUpSeializer
    def create(self, request):
        amount = int(request.data['amount'])*100
        client = razorpay.Client(auth =("rzp_test_ZWXABrcOqZkxq5" , "0MtQs5toufcReGw2kbWvvjqi"))
        payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
        

        try:
            wallet = Wallet.objects.get(user = self.request.user)
            print(wallet.id)
        except:
            raise AttributeError("Invalid User")

        # we are saving an order with keeping isPaid=False
        topUp = TopUp.objects.create(amount=amount,
                                    wallet=wallet,
                                    order_id = payment['id']
                                     )
        print(payment )
        return Response({'payment': payment })

@api_view(['POST'])
def handletopup(request):
    if request.method == "POST":
        a =  (request.POST)
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        order = TopUp.objects.filter(order_id = order_id).first()
        order.is_success = True
        orderamount = order.wallet.balance + (int(order.amount) / 100)
        Wallet.objects.filter(user=request.user).update(balance=orderamount)
        order.save

        return Response({"response":"Payment success"})
    else:
        return Response({"response":"Payment Failed"})
