# Generated by Django 4.2.3 on 2023-08-08 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_performancepost_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancepost',
            name='gender',
            field=models.CharField(default='무관', max_length=50),
        ),
    ]
