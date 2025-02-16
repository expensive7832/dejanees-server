# Generated by Django 5.0.6 on 2024-08-27 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_store',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='photoid',
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to='users'),
        ),
    ]
