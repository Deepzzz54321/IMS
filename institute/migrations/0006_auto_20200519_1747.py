# Generated by Django 3.0.6 on 2020-05-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0005_auto_20200519_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Added to Cart', 'Added to Cart'), ('Resolved', 'Resolved')], default='Pending', max_length=20),
        ),
    ]
