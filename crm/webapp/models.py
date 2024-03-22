from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    CAPACITY_CHOICES = [(i, i) for i in range(1, 7)]
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveSmallIntegerField(choices=CAPACITY_CHOICES)
    def __str__(self):

        return f'{self.number}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    check_in = models.DateField()

    check_out = models.DateField()

    def __str__(self):

        return self.first_name + "   " + self.last_name














