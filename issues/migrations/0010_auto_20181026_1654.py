# Generated by Django 2.1.2 on 2018-10-26 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_issue_repository'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
