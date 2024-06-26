# Generated by Django 4.2 on 2023-05-09 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0009_greener_wallet'),
        ('CompostersAccount', '0002_composter_groups_composter_is_superuser_and_more'),
        ('Blockchain', '0009_alter_transaction_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GreenersAccount.greener'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to='CompostersAccount.composter'),
        ),
    ]
