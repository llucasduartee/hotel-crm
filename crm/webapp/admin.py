from django.contrib import admin


from . models import Reservation, Room

admin.site.register(Reservation)
admin.site.register(Room)
