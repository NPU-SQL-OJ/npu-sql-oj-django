# Generated by Django 3.1.7 on 2022-02-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0038_auto_20220206_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='examquesanswerrec',
            name='score',
            field=models.IntegerField(default=0, verbose_name='本题得分'),
        ),
        migrations.AddField(
            model_name='exerquesanswerrec',
            name='score',
            field=models.IntegerField(default=0, verbose_name='本题得分'),
        ),
    ]
