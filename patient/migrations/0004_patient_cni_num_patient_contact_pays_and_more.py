# Generated by Django 4.2.19 on 2025-03-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_patient_cni_nni_patient_mere_patient_pere_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='cni_num',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='contact_pays',
            field=models.CharField(blank=True, help_text='Code ISO pays (ex: CI, FR)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='contact_second',
            field=models.CharField(db_index=True, default=0, max_length=225),
            preserve_default=False,
        ),
    ]
