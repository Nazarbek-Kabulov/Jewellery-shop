# Generated by Django 4.2.5 on 2023-10-09 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_comment_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
