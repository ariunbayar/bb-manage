# Generated by Django 2.1.2 on 2018-10-29 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0012_auto_20181029_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.CharField(max_length=255, null=True),
        ),
    ]