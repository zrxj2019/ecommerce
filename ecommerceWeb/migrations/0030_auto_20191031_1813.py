# Generated by Django 2.2.6 on 2019-10-31 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceWeb', '0029_questionrecord_test_testrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='time',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
