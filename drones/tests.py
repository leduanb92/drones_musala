from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from drones.models import Drone, Medication


class DroneTests(APITestCase):
    def setUp(self):
        Drone.objects.create(serial_number="DRN_1L", model="lightweight", weight_limit=250,  battery_capacity=50, state='idle')
        Drone.objects.create(serial_number="DRN_2M", model="middleweight", weight_limit=300,  battery_capacity=10, state='idle')
        Drone.objects.create(serial_number="DRN_3C", model="cruiserweight", weight_limit=400,  battery_capacity=60, state='delivering')
        Drone.objects.create(serial_number="DRN_4H", model="heavyweight", weight_limit=500,  battery_capacity=80, state='idle')
        Medication.objects.create(name='Advil-200', weight=100, code='ADV_200', image='/media/advil-200.jpg')
        Medication.objects.create(name='Advil-300', weight=300, code='ADV_300', image='/media/advil-300.jpg')

    def test_create_drone(self):
        """
        Ensure we can create a new Drone object.
        """
        url = reverse('drone-list')
        data = {
            'serial_number': 'DRN_1',
            'model': 'lightweight',
            'weight_limit': 250,
            'battery_capacity': 50,
            'state': 'idle'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_drone_fail(self):
        """
        Ensure we get a BAD REQUEST response if any field is not present, in this case the serial_number field.
        """
        url = reverse('drone-list')
        data = {
            'model': 'lightweight',
            'weight_limit': 250,
            'battery_capacity': 50,
            'state': 'idle'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'serial_number': [ErrorDetail('This field is required.', 'required')]})

    def test_check_battery_level(self):
        """
        Ensure we get an OK response when checking the battery level of an existing drone and that we get the correct
        value in the response body.
        """
        url = reverse('drone-check-battery-level', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['battery_level'], 50)

    def test_check_loaded_medications(self):
        """
        Ensure we get an OK response when checking the loaded medications on the drone and that we get a list
        containing its medications items.
        """
        url = reverse('drone-check-loaded-medications', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_available_drones(self):
        """
        Ensure we get an OK response when getting available drones. It should only return the ones with status 'idle'
        and with battery level greater than 25 percent.
        """
        url = reverse('drone-get-available-drones')
        response = self.client.get(url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)  # It should return two drones according to initial data
        self.assertTrue(data[0]['serial_number'] == 'DRN_4H')
        self.assertTrue(data[1]['serial_number'] == 'DRN_1L')

    def test_load_with_medication(self):
        """
        Ensure we get an OK response when loading a drone with existent medication and battery level above 25 percent.
        """
        url = reverse('drone-load-with-medication', kwargs={'pk': 1})
        response = self.client.post(url, {'medication_set': [1]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_load_with_nonexistent_medication(self):
        """
        Ensure we get a BAD REQUEST response when loading a drone with nonexistent medication.
        """
        url = reverse('drone-load-with-medication', kwargs={'pk': 1})
        response = self.client.post(url, {'medication_set': [20]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_load_with_medication_with_low_battery(self):
        """
        Ensure we get a CONFLICT response when loading a drone with low battery (lower than 25 percent).
        """
        url = reverse('drone-load-with-medication', kwargs={'pk': 2})
        response = self.client.post(url, {'medication_set': [1]})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('battery_capacity', response.data)
        self.assertEqual(response.data['battery_capacity'], ['This drone has less than 25% of battery, so it can not be loaded with medication.'])

    def test_load_with_medication_exceeding_weight(self):
        """
        Ensure we get a BAD REQUEST response when loading a drone with medication exceeding its weight limit.
        """
        url = reverse('drone-load-with-medication', kwargs={'pk': 1})  # Weight limit of 250g
        response = self.client.post(url, {'medication_set': [2]})  # It has a weight of 300g
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('medication_set', response.data)
