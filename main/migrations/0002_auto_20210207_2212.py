# Generated by Django 3.1.5 on 2021-02-07 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='optional',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=3),
        ),
    ]