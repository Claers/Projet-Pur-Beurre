# Generated by Django 2.1.4 on 2019-02-06 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webSite', '0007_remove_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorites',
        ),
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(to='webSite.Favorite'),
        ),
    ]
