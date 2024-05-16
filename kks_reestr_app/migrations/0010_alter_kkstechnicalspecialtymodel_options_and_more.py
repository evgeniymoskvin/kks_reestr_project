# Generated by Django 4.2.11 on 2024-05-14 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kks_reestr_app', '0009_kkstechnicalspecialtymodel_kks_tech_speciality_construction_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kkstechnicalspecialtymodel',
            options={'verbose_name': 'kks код технической специальности', 'verbose_name_plural': 'kks коды технических специальностей (сектор 7)'},
        ),
        migrations.AlterField(
            model_name='kkssector5model',
            name='kks_sector5_value',
            field=models.CharField(help_text='6 символов', max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Значение сектора 5'),
        ),
    ]