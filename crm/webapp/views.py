from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateReservationForm, UpdateReservationForm
from django.db import transaction
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .tasks import send_email_async
from django.contrib.auth.decorators import login_required
from .smtp import send_email_async
from .models import Reservation, Room

from django.contrib import messages




def home(request):

    return render(request, 'webapp/index.html')



def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)



def login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/login.html', context=context)




@login_required(login_url='login')
def dashboard(request):

    if request.user.is_staff:
        reservations = Reservation.objects.all()
    else:
        reservations = Reservation.objects.filter(user=request.user)
    

    context = {'reservations': reservations}

    return render(request, 'webapp/dashboard.html', context=context)




@login_required(login_url='login')
def create_reservation(request):
    form = CreateReservationForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        number_of_people = form.cleaned_data['number_of_people']

        with transaction.atomic():
     
            available_rooms = Room.objects.select_for_update().filter(capacity__gte=number_of_people,).exclude(reservation__check_in__lt=check_in,reservation__check_out__gt=check_out,)

            if not available_rooms.exists():
                form.add_error(None, 'No available rooms found for the selected dates and number of people.')
                return render(request, 'webapp/create-reservation.html', {'form': form})

            room = available_rooms.first()

   
            reservation = Reservation(
                first_name=first_name,
                last_name=last_name,
                email=email,
                room=room,
                check_in=check_in,
                check_out=check_out,
                user=request.user
            )
            reservation.save()
            
            send_email_async(
        'Your reservation was confirmed!',
        f'Your reservation from {reservation.check_in} to {reservation.check_out} has been confirmed',
        'lucasduartedsvp@gmail.com',
        [f'{reservation.email}']
    )

        return redirect('dashboard')

    context = {'form': form}
    return render(request, 'webapp/create-reservation.html', context=context)




@login_required(login_url='login')
def update_reservation(request, pk):

    reservation = Reservation.objects.get(id=pk)

    form = UpdateReservationForm(instance=reservation)

    if request.method == 'POST':

        form = UpdateReservationForm(request.POST, instance=reservation)

        if form.is_valid():

            form.save()
            send_email_async(
        'Your reservation was updated!',
        f'Your reservation from {reservation.check_in} to {reservation.check_out} has been updated',
        'lucasduartedsvp@gmail.com',
        [f'{reservation.email}']
    )
            messages.success(request, "Your reservation was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-reservation.html', context=context)




@login_required(login_url='login')
def singular_reservation(request, pk):

    reservation = Reservation.objects.get(id=pk)

    context = {'reservation': reservation}

    return render(request, 'webapp/reservation.html', context=context)




@login_required(login_url='login')
def cancel_reservation(request, pk):

    reservation = Reservation.objects.get(id=pk)

    send_email_async(
        'Your reservation was cancelled!',
        f'Your reservation from {reservation.check_in} to {reservation.check_out} has been cancelled',
        'lucasduartedsvp@gmail.com',
        [f'{reservation.email}']
    )

    reservation.delete()

    messages.success(request, "Your reservation was cancelled!")

    return redirect("dashboard")





def logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("login")



