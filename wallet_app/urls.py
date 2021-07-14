from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'create-topup',CreateTopUpViewset,basename='topup')
router.register(r'check-wallet',CreateWalletViewset,basename='topup')
router.register(r'create-transaction',CreateTransactionViewset,basename='topup')
router.register(r'create-type',CreateTypeViewset,basename='topup')
urlpatterns = [
        path('handlepayment/',handletopup,name="handlepayment"),
]
urlpatterns += router.urls