# Generated by Django 4.2 on 2023-05-01 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blockchain', '0004_alter_block_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='transaction',
            field=models.FloatField(),
        ),
    ]
