from rest_framework import serializers
from .models import FugitiveRecords

class FugitiveRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FugitivelRecords
        fields = ('firstname', 'lastname')
