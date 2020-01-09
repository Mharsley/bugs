from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from Bugs.models import Ticket
from Bugs.forms import LoginForm, NewTicket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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

    def __str__(self):
        return "{}, {}".format(self.Title, self.Name)
"""


@login_required
def index(request):
    html = "index.html"

    tickets = Ticket.objects.all()
    new = tickets.filter(Status='New').order_by("-Time")
    in_progress = tickets.filter(Status='In_progress').order_by("-Time")
    done = tickets.filter(Status='DONE').order_by("-Time")
    valid = tickets.filter(Status='VALID').order_by("-Time")

    return render(request, html, {
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'valid': valid
        })


def login_view(request):
    html = 'login_form.html'

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
                )

    form = LoginForm()

    return render(request, html, {'form': form})



@login_required
def add_ticket_view(request):
    html = 'generic_form.html'
    form = NewTicket()
    if request.method == "POST":
        form = NewTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                Title=data['Title'],
                Description=data['Description'],
                Status=data['Status'],
                Name=request.user,
                assigned=data['assigned']
            )
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def ticket_detail_view(request, id):
    html = 'ticket_detail.html'
    ticket = Ticket.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


@login_required
def edit_ticket_view(request, id):

    html = "generic_form.html"

    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = NewTicket(request.POST, instance=ticket)
        form.save()

        if ticket.Status == "DONE":
            ticket.completed = ticket.assigned
            ticket.assigned = None
            form.save()
        elif ticket.Status == "In_progress" and ticket.assigned is None:
            ticket.assigned = ticket.created_by
        elif ticket.Status == "VALID":
            ticket.completed = None
            ticket.assigned = None
            form.save()
        elif ticket.assigned is not None:
            ticket.Status = "In_progress"
            form.save()

        return HttpResponseRedirect(reverse('homepage'))

    form = NewTicket(instance=ticket)

    return render(request, html, {'form': form})


def user_view(request, id):
    html = 'users_page.html'

    created = Ticket.objects.filter(pk=id)
    assigned = Ticket.objects.filter(assigned=id)
    completed = Ticket.objects.filter(completed=id)

    return render(request, html,
                  {'created': created,
                   'assigned': assigned,
                   'completed': completed})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


