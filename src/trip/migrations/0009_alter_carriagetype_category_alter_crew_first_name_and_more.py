# Generated by Django 4.0.4 on 2025-02-28 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0008_ticket_unique_car_num_seat_num_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carriagetype',
            name='category',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='crew',
            name='first_name',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name='crew',
            name='last_name',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name='train',
            name='name_number',
            field=models.CharField(max_length=63),
        ),
    ]
