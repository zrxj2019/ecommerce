# Generated by Django 2.2.6 on 2019-10-03 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceWeb', '0016_questionrecord_test_testrecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionrecord',
            old_name='questionid',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='questionrecord',
            old_name='studentid',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='questionrecord',
            old_name='testid',
            new_name='test',
        ),
        migrations.RenameField(
            model_name='testrecord',
            old_name='studentid',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='testrecord',
            old_name='testid',
            new_name='test',
        ),
    ]
