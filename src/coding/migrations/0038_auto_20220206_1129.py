# Generated by Django 3.1.7 on 2022-02-06 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0037_auto_20220206_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examquesanswerrec',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coding.exam', verbose_name='对应考试'),
        ),
    ]
