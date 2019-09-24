# Generated by Django 2.1.1 on 2019-09-24 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceWeb', '0003_auto_20190924_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='studentid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ecommerceWeb.User'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacherid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ecommerceWeb.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, unique=True),
        ),
    ]
