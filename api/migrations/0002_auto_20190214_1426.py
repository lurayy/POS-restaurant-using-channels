# Generated by Django 2.1 on 2019-02-14 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderedItems',
            new_name='OrderedItem',
        ),
        migrations.AddField(
            model_name='order',
            name='table_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
