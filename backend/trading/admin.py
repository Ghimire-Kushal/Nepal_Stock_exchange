from django.contrib import admin
from .models import PaperTrade, PaperHolding, PaperWallet
admin.site.register((PaperTrade, PaperHolding, PaperWallet))
