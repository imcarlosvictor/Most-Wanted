from rest_framework import serializers
from .models import FugitiveProfiles

class FugitiveProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FugitiveProfiles
        fields = (
            'id',
            'name',
            'alias',
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
