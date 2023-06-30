# Generated by Django 4.1.4 on 2023-04-13 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('lid', models.AutoField(primary_key=True, serialize=False)),
                ('lreson', models.CharField(max_length=200)),
                ('lstart_date', models.DateField()),
                ('lend_date', models.DateField()),
                ('ldays', models.PositiveIntegerField(default=0)),
                ('lstatus', models.CharField(choices=[('APPROVAL', 'Approval'), ('NOTAPPROVAL', 'Not approval'), ('PENDING', 'Pending')], default='PENDING', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='User_Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infromation', models.CharField(default='', max_length=300)),
                ('skills', models.CharField(default='', max_length=100)),
            ],
        ),
    ]