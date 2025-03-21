# Generated by Django 5.1.6 on 2025-03-11 19:47

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treffen', '0018_category_category_type_alter_meetup_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='treffen.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.IntegerField(choices=[(1, 'Buddy'), (2, 'Meetup'), (3, 'Location')], default=1),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='date',
            field=models.DateField(default=datetime.date(2025, 3, 11)),
        ),
    ]
