# Generated by Django 3.2.10 on 2021-12-22 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transplants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biopsy',
            name='donor_ref',
        ),
        migrations.RemoveField(
            model_name='biopsy',
            name='recipient_ref',
        ),
        migrations.RemoveField(
            model_name='biopsy',
            name='transplant_date',
        ),
        migrations.RemoveField(
            model_name='histology',
            name='biopsy_date',
        ),
        migrations.RemoveField(
            model_name='histology',
            name='donor_ref',
        ),
        migrations.RemoveField(
            model_name='histology',
            name='recipient_ref',
        ),
        migrations.RemoveField(
            model_name='histology',
            name='transplant_date',
        ),
        migrations.RemoveField(
            model_name='sequencingdata',
            name='biopsy_date',
        ),
        migrations.RemoveField(
            model_name='sequencingdata',
            name='donor_ref',
        ),
        migrations.RemoveField(
            model_name='sequencingdata',
            name='recipient_ref',
        ),
        migrations.RemoveField(
            model_name='sequencingdata',
            name='transplant_date',
        ),
    ]