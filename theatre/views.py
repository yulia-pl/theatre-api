from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TheatreHall, Play, Genre, Actor, Performance, Reservation, Ticket
from .serializers import (
    TheatreHallSerializer,
    PlaySerializer,
    GenreSerializer,
    ActorSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
)


class TheatreHallListCreateView(generics.ListCreateAPIView):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayListCreateView(generics.ListCreateAPIView):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorListCreateView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PerformanceListCreateView(generics.ListCreateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class PerformanceListView(generics.ListAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["play__title", "theatre_hall__name", "show_time"]
    ordering_fields = ["show_time"]
