# Generated by Django 3.0.3 on 2020-03-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jovem', '0008_auto_20200315_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='usuario_photos'),
        ),
    ]
