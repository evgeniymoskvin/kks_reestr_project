# Generated by Django 4.2.11 on 2024-05-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kks_reestr_app', '0013_alter_kkssector6model_kks_sector6_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kkscodemodel',
            name='text',
            field=models.CharField(max_length=37, unique=True, verbose_name='Kks код'),
        ),
    ]
