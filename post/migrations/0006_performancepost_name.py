# Generated by Django 4.2.4 on 2023-08-11 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_performancepost_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancepost',
            name='name',
            field=models.CharField(default='이름', max_length=50),
        ),
    ]
