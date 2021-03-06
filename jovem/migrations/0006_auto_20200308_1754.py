# Generated by Django 3.0.3 on 2020-03-08 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jovem', '0005_auto_20200308_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jovem.Instituicao'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='jovem.TipoUser'),
        ),
    ]
