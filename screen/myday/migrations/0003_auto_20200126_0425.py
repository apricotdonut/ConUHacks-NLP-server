# Generated by Django 3.0.2 on 2020-01-26 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myday', '0002_auto_20200126_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myjournal',
            name='date_created',
            field=models.DateField(verbose_name='journal date'),
        ),
    ]
