from django.contrib import admin
from .models import Stock, Associate, StocksOwned, Account, Transaction

# Register your models here.


admin.site.register(Stock)
admin.site.register(Associate)
admin.site.register(StocksOwned)
admin.site.register(Account)
admin.site.register(Transaction)