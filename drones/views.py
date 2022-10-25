from rest_framework import viewsets

from drones.serializers import DroneSerializer, MedicationSerializer
from drones.models import Drone, Medication


class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Drones to be viewed or edited.
    """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Medications to be viewed or edited.
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
