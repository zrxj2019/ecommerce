# Generated by Django 2.2.6 on 2019-10-22 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceWeb', '0017_auto_20191003_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrecord',
            name='student',
        ),
        migrations.RemoveField(
            model_name='testrecord',
            name='test',
        ),
        migrations.DeleteModel(
            name='QuestionRecord',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='TestRecord',
        ),
    ]
