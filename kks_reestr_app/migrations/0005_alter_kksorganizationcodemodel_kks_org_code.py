# Generated by Django 4.2.11 on 2024-05-03 11:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kks_reestr_app', '0004_remove_kksorganizationcodemodel_kks_org_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kksorganizationcodemodel',
            name='kks_org_code',
            field=models.CharField(help_text='3 символа', max_length=3, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Код организации'),
        ),
    ]
