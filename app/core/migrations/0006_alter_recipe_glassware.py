# Generated by Django 4.0.4 on 2022-05-22 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='glassware',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
