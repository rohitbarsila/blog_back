# Generated by Django 3.0.5 on 2020-04-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_data', '0003_auto_20200422_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, to='Blog_data.tags'),
        ),
    ]
