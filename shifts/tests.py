from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from .models import Worker, Shift


class ShiftValidationTests(APITestCase):
    def setUp(self):
        self.worker1 = Worker.objects.create(name='Asad')
        self.worker2 = Worker.objects.create(name='Iqbal')

        self.shift1 = Shift.objects.create(
            worker=self.worker1,
            start_time=datetime(2022, 1, 1, 8),
            end_time=datetime(2022, 1, 1, 16)
        )
        self.shift2 = Shift.objects.create(
            worker=self.worker2,
            start_time=datetime(2022, 1, 1, 0),
            end_time=datetime(2022, 1, 1, 8)
        )

    def test_create_shift_valid(self):
        url = reverse('shift-list')
        data = {'worker': self.worker1.id, 'start_time': '2022-01-02T08:00:00Z', 'end_time': '2022-01-02T16:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shift.objects.count(), 3)

    def test_worker_already_has_shift_on_same_day(self):
        url = reverse('shift-list')
        data = {'worker': self.worker1.id, 'start_time': '2022-01-01T08:00:00Z', 'end_time': '2022-01-01T16:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Worker already has a shift on this day'])

    def test_create_shift_invalid_start_end_time(self):
        url = reverse('shift-list')
        data = {'worker': self.worker1.id, 'start_time': '2022-01-02T09:00:00Z', 'end_time': '2022-01-02T17:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Shifts 24 hour timetable must be 0-8, 8-16, 16-24'])

    def test_create_shift_invalid_duration(self):
        url = reverse('shift-list')
        data = {'worker': self.worker1.id, 'start_time': '2022-01-02T00:00:00Z', 'end_time': '2022-01-02T16:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Shift duration must be exactly 8 hours'])
