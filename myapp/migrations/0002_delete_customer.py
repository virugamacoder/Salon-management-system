# Generated by Django 4.2 on 2023-04-14 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_feedback_cid'),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
