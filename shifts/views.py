from rest_framework import generics
from .models import Worker, Shift
from .serializers import WorkerSerializer, ShiftSerializer


class ShiftList(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class WorkerList(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
