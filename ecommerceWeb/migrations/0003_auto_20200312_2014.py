# Generated by Django 2.1.5 on 2020-03-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceweb', '0002_auto_20200312_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
