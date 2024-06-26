# Generated by Django 4.2 on 2023-05-23 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0009_greener_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenerNotifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Message', models.CharField(max_length=255)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('IsRead', models.BooleanField(default=False)),
                ('greener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='greener', to='GreenersAccount.greener')),
            ],
            options={
                'ordering': ['-Timestamp'],
            },
        ),
    ]
