# Generated by Django 3.2.7 on 2021-09-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0007_auto_20210926_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='day_highest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='stock',
            name='day_lowest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='stock',
            name='p_e',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=14),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]
