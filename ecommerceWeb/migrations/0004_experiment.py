# Generated by Django 2.1.5 on 2020-01-06 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceweb', '0003_topic_topictype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('experimentid', models.AutoField(primary_key=True, serialize=False)),
                ('experimentname', models.CharField(max_length=200)),
                ('experimentfile', models.CharField(max_length=200)),
            ],
        ),
    ]