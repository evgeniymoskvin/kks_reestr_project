# Generated by Django 4.2.11 on 2024-05-06 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kks_reestr_app', '0007_remove_kksbuildingmodel_kks_object_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kksbuildingmodel',
            name='kks_object',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='kks_reestr_app.kksobjectmodel', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='kkstypebuildingmodel',
            name='kks_type_building_description',
            field=models.CharField(max_length=150, verbose_name='Описание'),
        ),
    ]
