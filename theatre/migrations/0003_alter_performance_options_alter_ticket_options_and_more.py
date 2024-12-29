# Generated by Django 5.1.4 on 2024-12-26 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0002_actor_genre_play_alter_theatrehall_rows_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="performance",
            options={"ordering": ["show_time"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AddField(
            model_name="play",
            name="actors",
            field=models.ManyToManyField(
                blank=True, related_name="plays", to="theatre.actor"
            ),
        ),
        migrations.AddField(
            model_name="play",
            name="genres",
            field=models.ManyToManyField(
                blank=True, related_name="plays", to="theatre.genre"
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="play",
            name="title",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="theatrehall",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="performance",
            unique_together={("theatre_hall", "show_time")},
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("performance", "row", "seat")},
        ),
    ]
