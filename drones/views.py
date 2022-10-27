from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from drones.serializers import DroneSerializer, MedicationSerializer, LoadMedicationDroneSerializer
from drones.models import Drone, Medication


class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Drones to be viewed or edited.
    It also allows to make the following requests:
    - Load a drone with medication.
    - Check loaded medications of a specified drone.
    - Check battery level of a specified drone.
    - Get available drones for loading.
    """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'load_with_medication':
            serializer_class = LoadMedicationDroneSerializer

        return serializer_class

    @action(methods=['post'], detail=True)
    def load_with_medication(self, request, pk=None):
        """
        Load a drone with medication.
        """
        drone = get_object_or_404(self.get_queryset(), id=pk)
        if drone.battery_capacity < 25:
            error = {
                'battery_capacity': [
                    'This drone has less than 25% of battery, so it can not be loaded with medication.'
                ]
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer_class()(drone, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(state=Drone.STATE_LOADED)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def check_loaded_medications(self, request, pk=None):
        """
        Check loaded medications of a specified drone.
        """
        drone = get_object_or_404(self.get_queryset(), id=pk)
        medications_serializer = MedicationSerializer(drone.medication_set, many=True, context={'request': request})
        return Response(medications_serializer.data)

    @action(methods=['get'], detail=True)
    def check_battery_level(self, request, pk=None):
        """
        Check battery level of a specified drone.
        """
        drone = get_object_or_404(self.get_queryset(), id=pk)
        data = {'battery_level': drone.battery_capacity}
        return Response(data)

    @action(methods=['get'], detail=False)
    def get_available_drones(self, request):
        """
        Get available drones for loading.
        """
        available_drones = self.get_queryset().filter(state=Drone.STATE_IDLE)
        serializer = self.get_serializer_class()(available_drones, many=True, context={'request': request})
        return Response(serializer.data)


class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Medications to be viewed or edited.
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
