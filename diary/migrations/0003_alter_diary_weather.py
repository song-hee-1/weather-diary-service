# Generated by Django 4.1.1 on 2022-09-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_diary_weather_alter_diary_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='weather',
            field=models.CharField(default=None, max_length=20, null=True, verbose_name='날씨'),
        ),
    ]