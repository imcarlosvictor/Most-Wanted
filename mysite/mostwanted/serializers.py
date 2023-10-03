from rest_framework import serializers
from .models import CriminalRecords

class CriminalRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriminalRecords
        fields = ('firstname', 'lastname')
