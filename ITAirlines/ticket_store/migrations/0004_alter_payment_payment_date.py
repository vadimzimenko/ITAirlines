# Generated by Django 5.0.2 on 2024-04-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_store', '0003_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата та час транзакції'),
        ),
    ]