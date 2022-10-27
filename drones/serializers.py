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
class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    image = Base64ContentField(required=False)

    class Meta:
        model = Medication
        fields = ['id', 'url', 'name', 'weight', 'code', 'image', 'drone']


class MedicationInDroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Medication
        fields = ['id', 'url', 'name', 'weight', 'code', 'image']


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    medication_set = MedicationInDroneSerializer(many=True, read_only=True)

    class Meta:
        model = Drone
        fields = ['id', 'url', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state', 'medication_set']


class LoadMedicationDroneSerializer(serializers.HyperlinkedModelSerializer):
    medication_set = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), many=True, required=True)

    class Meta:
        model = Drone
        fields = ['id', 'url', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state', 'medication_set']
        read_only_fields = ['id', 'url', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state']

    def validate_medication_set(self, medications):
        """
        Check that total weight of medications do NOT surpass weight limit of drone.
        """
        total_weight = 0
        for medication in medications:
            total_weight += medication.weight

        if total_weight > self.instance.weight_limit:
            raise serializers.ValidationError(f"This drone has a weight limit of {self.instance.weight_limit}g. The total "
                                              f"weight of medications was {total_weight}g")
        return medications
