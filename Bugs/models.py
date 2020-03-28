from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Ticket(models.Model):
    Title = models.CharField(max_length=50)
    Time = models.DateTimeField(default=timezone.now)
    Description = models.TextField()
    Name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Name',
        blank=True, null=True

    )

    Status = models.CharField(
        max_length=200,
        default="New",
        )
    assigned = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned',
        blank=True, null=True
        )
    completed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='completed',
        blank=True,
        null=True
    )

    def __str__(self):
        return "{}, {}".format(self.Title, self.Name)
           