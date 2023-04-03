from django.urls import path
from .views import ShiftList, WorkerList


urlpatterns = [
    # List all workers or create a new worker
    path('workers/', WorkerList.as_view(), name='worker-list'),

    # List all shifts or create a new shift
    path('shifts/', ShiftList.as_view(), name='shift-list'),
]
