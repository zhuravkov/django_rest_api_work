# Generated by Django 4.0.3 on 2022-03-20 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0007_alter_orderinwork_options_orderindone'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderInWork',
        ),
    ]
