from django.contrib import admin

from .models import Customers
from .models import Flights

from myapp.views import newsched

# Register your models here.
#Add models to the admin page
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName', '=bookingNo']

class FlightAdmin(admin.ModelAdmin):
    search_fields = ['=flightNo', 'planeType']

#Register models on admin page
admin.site.register(Customers, CustomerAdmin)
admin.site.register(Flights, FlightAdmin)

#Add function to be able to create required flights at once
admin.site.add_action(newsched, 'Create set of new flights')
