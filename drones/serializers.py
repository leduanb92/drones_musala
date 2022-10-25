import base64
import uuid

from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.validators import UniqueValidator

from drones.models import Drone, Medication


class Base64ContentField(Field):
    """
    For image, send base64 string as json
    """

    def to_internal_value(self, data):
        try:
            format, datastr = data.split(';base64,')
            ext = format.split('/')[-1]
            file = ContentFile(base64.b64decode(datastr), name=str(uuid.uuid4())+'.'+ext)
        except:
            raise serializers.ValidationError('Error in decoding base64 data')
        return file

    def to_representation(self, value):
        if not value:
            return None
        return value.url


# Serializers define the API representation.
class DroneSerializer(serializers.HyperlinkedModelSerializer):
    medications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Drone
        fields = ['id', 'url', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state', 'medications']
        validators = [
            UniqueValidator(
                queryset=Drone.objects.all(),
                message=_('Drones must have unique serial numbers.')
            )
        ]


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    image = Base64ContentField(required=False)

    class Meta:
        model = Medication
        fields = ['id', 'url', 'name', 'weight', 'code', 'image', 'drone']
