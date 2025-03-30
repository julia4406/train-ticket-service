from django.contrib import admin

from trip import models

admin.site.register(models.Train)
admin.site.register(models.CarriageType)
admin.site.register(models.Ticket)
admin.site.register(models.Order)
admin.site.register(models.Trip)
admin.site.register(models.Route)
admin.site.register(models.Crew)
admin.site.register(models.Station)
