from django.contrib import admin
from  . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Staff)
admin.site.register(models.Trustedclient)
admin.site.register(models.Address)
admin.site.register(models.Counter)
admin.site.register(models.Phone)
admin.site.register(models.Project)
admin.site.register(models.Testimonial)

