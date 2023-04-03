from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Worker, Shift


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source='worker.name', read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'start_time', 'end_time', 'worker', 'worker_name']

    def validate(self, data):
        # Check if the worker already has a shift on the selected day
        worker = data['worker']
        start_time = data['start_time']
        end_time = data['end_time']
        shifts = Shift.objects.filter(worker=worker, start_time__date=start_time.date())
        if shifts:
            raise ValidationError("Worker already has a shift on this day")

        if start_time.hour not in [0, 8, 16] or end_time.hour not in [8, 16, 24]:
            raise ValidationError("Shifts 24 hour timetable must be 0-8, 8-16, 16-24")

        # Check if shift is exactly 8 hours long
        if (end_time - start_time) != timedelta(hours=8):
            raise serializers.ValidationError("Shift duration must be exactly 8 hours")

        return data
