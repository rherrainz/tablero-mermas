# Generated by Django 5.2.3 on 2025-06-30 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('suc_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('zona', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
            ],
        ),
    ]
