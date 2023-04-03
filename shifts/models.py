from django.db import models


class Shift(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)


class Worker(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
