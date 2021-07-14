from django.db.models.fields.related import OneToOneField
from users.models import User
from django.db import models
import uuid
# Type of Request

class Type(models.Model):
    name = models.CharField(max_length=50)

# Wallet linked to User
class Wallet(models.Model):
    balance = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

# Transaction Done with Wallets
# all type of debits and credits will be done in transation model
#transaction model will generate Transaction id and refference id on each transaction 

class Transaction(models.Model):
    credited_to = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="credited_to_wallet")
    debited_wallet =  models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="debited_to_wallet")
    transaction_id = models.CharField(max_length=10,default=uuid.uuid4,blank=True)
    refference_id = models.CharField(max_length=10,default=uuid.uuid4,blank=True)
    is_success = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    # type = models.ManyToManyField(Type)
    # def save(self,*args, **kwargs):
    #     self.debited_wallet.balance = self.debited_wallet.balance - self.amount
    #     self.credited_to.balance = self.credited_to.balance + self.amount
    #     self.debited_wallet.save()
    #     self.credited_to.save()
    #     super(Transaction, self).save(*args, **kwargs)
class TopUp(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=1000 )
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    description = models.CharField(max_length=50, default="None")
    is_success = models.BooleanField(default=False)
    # def save(self,*args, **kwargs):
    #     self.wallet.balance = self.wallet.balance + self.amount
    #     self.wallet.save()
    #     super(TopUp, self).save(*args, **kwargs)
    