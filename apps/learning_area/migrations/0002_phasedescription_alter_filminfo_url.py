# Generated by Django 5.0 on 2024-02-03 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_area', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhaseDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='起始時間')),
                ('end', models.DateTimeField(verbose_name='結尾時間')),
                ('description', models.CharField(max_length=20, verbose_name='段落重點')),
            ],
        ),
        migrations.AlterField(
            model_name='filminfo',
            name='url',
            field=models.URLField(max_length=256, verbose_name='網址'),
        ),
    ]