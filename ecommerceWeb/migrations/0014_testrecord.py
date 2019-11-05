# Generated by Django 2.2.6 on 2019-10-02 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceWeb', '0013_delete_testrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestRecord',
            fields=[
                ('recordid', models.AutoField(primary_key=True, serialize=False)),
                ('testname', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('state', models.IntegerField()),
                ('score', models.IntegerField()),
                ('studentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceWeb.Student')),
            ],
        ),
    ]
