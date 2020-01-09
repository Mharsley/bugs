from django import forms
from Bugs.models import Ticket
"""
    Title = models.CharField(max_length=50)
    Time = models.DateTimeField()
    Description = models.CharField(max_length=50)
    Name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name')

    NEW = 'New'
    IN_PROGRESS = 'In_progress'
    DONE = 'DONE'
    VALID = 'VALID'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In_progress'),
        (DONE, 'Done'),
        (VALID, 'Valid')
    ]

    Status = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        default=NEW,
        )
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned', blank=True, null=True)
    completed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed', blank=True, null=True)
 """


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class NewTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'Title',
            'Description',
            'Status',
            'assigned'
        ]
