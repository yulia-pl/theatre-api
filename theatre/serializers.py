from rest_framework import serializers
from .models import TheatreHall, Play, Genre, Actor, Performance, Reservation, Ticket


class TheatreHallSerializer(serializers.ModelSerializer):
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row", "total_seats"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["total_seats"] = instance.total_seats()
        return representation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name"]


class PlaySerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]

    def create(self, validated_data):
        genres_data = self.initial_data.get("genres", [])
        actors_data = self.initial_data.get("actors", [])
        play = Play.objects.create(**validated_data)

        play.genres.set(Genre.objects.filter(id__in=genres_data))
        play.actors.set(Actor.objects.filter(id__in=actors_data))
        return play


class PerformanceSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)
    available_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "play",
            "play_title",
            "theatre_hall",
            "theatre_hall_name",
            "show_time",
            "available_tickets",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["available_tickets"] = instance.available_tickets()
        return representation


class ReservationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    total_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "user_username", "total_tickets"]
        extra_kwargs = {"user": {"read_only": True}}

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["total_tickets"] = instance.total_tickets()
        return representation




class TicketSerializer(serializers.ModelSerializer):
    performance_title = serializers.CharField(source="performance.play.title", read_only=True)
    theatre_hall_name = serializers.CharField(source="performance.theatre_hall.name", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "performance_title", "theatre_hall_name", "reservation"]

    def validate(self, attrs):
        performance = attrs.get("performance")
        row = attrs.get("row")
        seat = attrs.get("seat")

        if row > performance.theatre_hall.rows:
            raise serializers.ValidationError(f"Row {row} exceeds maximum rows for this theatre hall.")
        if seat > performance.theatre_hall.seats_in_row:
            raise serializers.ValidationError(f"Seat {seat} exceeds maximum seats for this theatre hall.")
        return attrs
