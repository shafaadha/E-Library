# Generated by Django 5.1.3 on 2024-11-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0004_bookmodel_keywords_bookmodel_page_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='page_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]