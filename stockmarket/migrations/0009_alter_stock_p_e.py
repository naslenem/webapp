# Generated by Django 3.2.7 on 2021-09-26 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0008_auto_20210926_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='p_e',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
