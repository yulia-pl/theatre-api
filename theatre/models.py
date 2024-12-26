from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TheatreHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def clean(self):
        if self.rows <= 0:
            raise ValidationError("Number of rows must be greater than zero.")
        if self.seats_in_row <= 0:
            raise ValidationError("Number of seats in a row must be greater than zero.")

    def total_seats(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} (Total seats: {self.total_seats()})"


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Play(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="plays", blank=True)
    actors = models.ManyToManyField(Actor, related_name="plays", blank=True)

    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    class Meta:
        unique_together = ("theatre_hall", "show_time")
        ordering = ["show_time"]

    def available_tickets(self):
        total_tickets = self.theatre_hall.total_seats()
        sold_tickets = self.tickets.count()
        return total_tickets - sold_tickets

    def __str__(self):
        return f"{self.play.title} in {self.theatre_hall.name} on {self.show_time:%Y-%m-%d %H:%M}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_tickets(self):
        return self.tickets.count()

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.created_at:%Y-%m-%d}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]

    def clean(self):
        if self.row > self.performance.theatre_hall.rows:
            raise ValidationError(
                f"Row {self.row} exceeds the maximum rows in the theatre hall."
            )
        if self.seat > self.performance.theatre_hall.seats_in_row:
            raise ValidationError(
                f"Seat {self.seat} exceeds the maximum seats in a row."
            )

    def __str__(self):
        return f"Ticket for {self.performance.play.title} (Row {self.row}, Seat {self.seat})"
