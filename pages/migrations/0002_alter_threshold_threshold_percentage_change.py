# Generated by Django 4.1 on 2022-11-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threshold',
            name='threshold_percentage_change',
            field=models.DecimalField(decimal_places=2, help_text='Enter the stock threshold percentage change content', max_digits=5, null=True),
        ),
    ]