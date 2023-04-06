from rest_framework import serializers
from mangos.models import mangosModel

class mangosSerializer(serializers.ModelSerializer):
    class Meta:
        model = mangosModel
        fields = ('imagen',)