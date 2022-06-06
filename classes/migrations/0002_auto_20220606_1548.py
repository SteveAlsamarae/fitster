# Generated by Django 3.2.8 on 2022-06-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Facebook Link'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='instagram',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Instagram Link'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Twitter Link'),
        ),
    ]