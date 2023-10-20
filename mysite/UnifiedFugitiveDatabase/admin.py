from django.contrib import admin
from .models import FugitiveProfiles

# Register your models here.
admin.site.register(FugitiveProfiles)

class FugitiveProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'alias',
        'sex',
        'height',
        'weight',
        'eyes',
        'hair',
        'distinguishing_marks',
        'nationality',
        'date_of_birth',
        'place_of_birth',
        'charges',
        'wanted_by',
        'status',
        'publication',
        'last_modified',
        'reward',
        'details',
        'caution',
        'remarks',
        'images',
        'link',
    )

    list_filter = (
        'sex',
        'charges',
        'wanted_by',
        'status',
    )
