# Generated by Django 3.2.7 on 2021-09-26 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0005_alter_stock_point_q'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=14),
        ),
    ]
