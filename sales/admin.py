from django.contrib import admin
from .models import Ticketsale, Airline, Destination, Route, Adults, Childs, Infants
# Register your models here.

admin.site.register(Ticketsale)
admin.site.register(Airline)
admin.site.register(Destination)
admin.site.register(Route)
admin.site.register(Adults)
admin.site.register(Childs)
admin.site.register(Infants)