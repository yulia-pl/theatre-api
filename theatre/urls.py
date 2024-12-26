from django.urls import path
from .views import (
    TheatreHallListCreateView,
    PlayListCreateView,
    GenreListCreateView,
    ActorListCreateView,
    PerformanceListCreateView,
    ReservationListCreateView,
    TicketListCreateView,
)

urlpatterns = [
    path("theatre-halls/", TheatreHallListCreateView.as_view(), name="theatre-halls"),
    path("plays/", PlayListCreateView.as_view(), name="plays"),
    path("genres/", GenreListCreateView.as_view(), name="genres"),
    path("actors/", ActorListCreateView.as_view(), name="actors"),
    path("performances/", PerformanceListCreateView.as_view(), name="performances"),
    path("reservations/", ReservationListCreateView.as_view(), name="reservations"),
    path("tickets/", TicketListCreateView.as_view(), name="tickets"),
]
