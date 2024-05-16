# Generated by Django 4.2.11 on 2024-05-15 10:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kks_reestr_app', '0010_alter_kkstechnicalspecialtymodel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KKSThematicDirectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kks_thematic_direction_abr', models.CharField(help_text='По таблице приложения Д', max_length=3, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Код тематического направления работы')),
                ('kks_thematic_direction_description', models.CharField(blank=True, max_length=250, verbose_name='Описание кода')),
                ('kks_thematic_direction_visible', models.BooleanField(verbose_name='Видимость')),
            ],
            options={
                'verbose_name': 'kks код тематического направления работы',
                'verbose_name_plural': 'kks коды тематических направлений работы',
            },
        ),
    ]