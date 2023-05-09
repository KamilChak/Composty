# Generated by Django 4.2 on 2023-05-09 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GreenersAccount', '0009_greener_wallet'),
        ('CompostersAccount', '0002_composter_groups_composter_is_superuser_and_more'),
        ('Blockchain', '0010_alter_transaction_recipient_alter_transaction_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CompostersAccount.composter'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to='GreenersAccount.greener'),
        ),
    ]