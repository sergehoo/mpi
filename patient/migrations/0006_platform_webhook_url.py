# Generated by Django 4.2.19 on 2025-03-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_alter_patient_cni_nni_alter_patient_cni_num_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='webhook_url',
            field=models.URLField(blank=True, help_text='URL de notification de la plateforme', null=True),
        ),
    ]
