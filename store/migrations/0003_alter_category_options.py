# Generated by Django 5.0.6 on 2025-01-09 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
