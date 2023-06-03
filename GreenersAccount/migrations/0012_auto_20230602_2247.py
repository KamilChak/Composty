# Generated by Django 4.2 on 2023-06-02 21:30

from django.db import migrations
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0011_greener_composterstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GreenersAccount.greener')),
                ('manure', models.FloatField()),
                ('brown_material', models.FloatField()),
                ('green_material', models.FloatField()),
                ('date_range_start', models.DateField()),
                ('date_range_end', models.DateField()),
                ('Status', models.CharField(choices=[('completed', 'Completed'),('pending', 'Pending'),('declined', 'Declined'),('expired', 'Expired')], default='waiting', max_length=50)),
            ],
        ),
    ]