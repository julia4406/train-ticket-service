# Generated by Django 4.0.4 on 2025-02-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_alter_train_total_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='carriagetype',
            name='seats_in_car',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='train',
            name='carriages_quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
