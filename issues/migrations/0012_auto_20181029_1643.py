# Generated by Django 2.1.2 on 2018-10-29 08:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0011_issue_issue_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='created_at_bb',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 8, 43, 33, 788886, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='updated_at_bb',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 8, 43, 38, 628797, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
