# Generated by Django 3.2.19 on 2023-05-30 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('date_time', models.DateTimeField()),
            ],
        ),
    ]
