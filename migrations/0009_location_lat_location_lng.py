# Generated by Django 5.1.4 on 2025-01-15 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treffen', '0008_alter_meetup_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='location',
            name='lng',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
