# Generated by Django 2.1.2 on 2018-10-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0014_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='assignee',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at_bb',
            field=models.DateTimeField(null=True),
        ),
    ]
