# Generated by Django 3.0b1 on 2020-08-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApp', '0003_auto_20200824_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produkty',
            name='kategoria',
            field=models.CharField(choices=[('inne', 'Inne'), ('owoce', 'Owoce'), ('warzywa', 'Warzywa'), ('zboża', 'Zboza'), ('nabiał', 'Nabial'), ('mięso', 'Mieso'), ('ryby', 'Ryby'), ('przyprawy', 'Przyprawy')], default='inne', max_length=20),
        ),
    ]
