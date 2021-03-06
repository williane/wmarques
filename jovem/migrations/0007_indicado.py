# Generated by Django 3.0.3 on 2020-03-15 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jovem', '0006_auto_20200308_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='indicado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('nome', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('documento', models.FileField(blank=True, null=True, upload_to='doc_indicado')),
                ('resp_indicacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jovem.Usuario')),
            ],
        ),
    ]
