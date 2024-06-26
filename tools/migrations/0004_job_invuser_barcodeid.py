# Generated by Django 5.0.6 on 2024-06-18 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_alter_supply_quantityreplenished'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('barcodeID', models.CharField(max_length=255, unique=True)),
                ('isBeingWorkedOn', models.BooleanField()),
                ('timeScannedIn', models.DateTimeField(blank=True, null=True)),
                ('userScannedIn', models.CharField(blank=True, max_length=50)),
                ('totalHours', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='invuser',
            name='barcodeID',
            field=models.CharField(default='123', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
