# Generated by Django 3.0.3 on 2020-04-11 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jovem', '0015_auto_20200410_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituicao',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
