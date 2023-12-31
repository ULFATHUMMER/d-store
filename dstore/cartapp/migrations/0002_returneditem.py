# Generated by Django 4.2.4 on 2023-11-23 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0001_initial'),
        ('cartapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartapp.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.product')),
            ],
            options={
                'db_table': 'ReturnedItem',
            },
        ),
    ]
