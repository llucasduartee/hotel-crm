
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('login', views.login, name="login"),

    path('logout', views.logout, name="logout"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-reservation', views.create_reservation, name="create-reservation"),

    path('update-reservation/<int:pk>', views.update_reservation, name='update-reservation'),

    path('reservation/<int:pk>', views.singular_reservation, name="reservation"),

    path('cancel-reservation/<int:pk>', views.cancel_reservation, name="cancel-reservation"),

    path('rooms', views.rooms, name="rooms"),
    path('create-room', views.create_room, name="create-room"),
    path('update-room/<int:pk>', views.update_room, name="update-room"),
    path('delete-room/<int:pk>', views.delete_room, name="delete-room"),
    path('room/<int:pk>', views.singular_room, name="room"),
    

]






