# Generated by Django 3.0.3 on 2020-03-15 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jovem', '0010_indicado_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicado',
            name='valor_comissao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='indicado',
            name='valor_cotacao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]