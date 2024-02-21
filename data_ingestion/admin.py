from django.contrib import admin
from .models import PointOfInterest
# Register your models here.
class PointOfInterestAdmin(admin.ModelAdmin):
    exclude = ['description', ]
    search_fields = ('id', 'external_id')
    list_filter = ('category',)

admin.site.register(PointOfInterest, PointOfInterestAdmin)