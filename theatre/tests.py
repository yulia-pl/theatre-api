from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from theatre.models import (
    TheatreHall,
    Genre,
    Actor,
    Play,
    Performance,
    Reservation,
    Ticket
)


class TheatreAPITestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username="test_user", password="password")
        self.client.force_authenticate(user=self.user)

        # Theatre Hall
        self.theatre_hall_data = {
            "name": "Main Hall",
            "rows": 10,
            "seats_in_row": 15
        }
        self.theatre_hall = TheatreHall.objects.create(**self.theatre_hall_data)

        # Genre
        self.genre = Genre.objects.create(name="Drama")

        # Actor
        self.actor = Actor.objects.create(first_name="William", last_name="Shakespeare")

        # Play
        self.play = Play.objects.create(title="Hamlet", description="A tragedy.")
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

        # Performance
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-12-31T19:00:00Z"
        )

        # Reservation
        self.reservation = Reservation.objects.create(user=self.user)

        # Ticket
        self.ticket = Ticket.objects.create(
            row=5,
            seat=7,
            performance=self.performance,
            reservation=self.reservation
        )

    def test_get_theatre_halls(self):
        response = self.client.get("/api/theatre-halls/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.theatre_hall_data["name"])

    def test_create_theatre_hall(self):
        new_hall_data = {
            "name": "Small Hall",
            "rows": 5,
            "seats_in_row": 8
        }
        response = self.client.post("/api/theatre-halls/", new_hall_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TheatreHall.objects.count(), 2)
        self.assertEqual(TheatreHall.objects.last().name, new_hall_data["name"])

    def test_get_plays(self):
        response = self.client.get("/api/plays/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.play.title)

    def test_create_play(self):
        new_play_data = {
            "title": "Othello",
            "description": "Another tragedy.",
            "genres": [self.genre.id],
            "actors": [self.actor.id]
        }
        response = self.client.post("/api/plays/", new_play_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 2)
        self.assertEqual(Play.objects.last().title, new_play_data["title"])

    def test_get_performances(self):
        response = self.client.get("/api/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["play_title"], self.performance.play.title)

    def test_create_performance(self):
        new_performance_data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2025-01-01T20:00:00Z"
        }
        response = self.client.post("/api/performances/", new_performance_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)

    def test_get_reservations(self):
        response = self.client.get("/api/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_username"], self.user.username)

    def test_create_reservation(self):
        response = self.client.post("/api/reservations/", {})
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_get_tickets(self):
        response = self.client.get("/api/tickets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["row"], self.ticket.row)

    def test_create_ticket(self):
        new_ticket_data = {
            "row": 6,
            "seat": 8,
            "performance": self.performance.id,
            "reservation": self.reservation.id
        }
        response = self.client.post("/api/tickets/", new_ticket_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)
