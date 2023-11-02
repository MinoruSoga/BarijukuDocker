# Generated by Django 4.1.7 on 2023-11-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='有効かどうか'),
        ),
        migrations.AlterField(
            model_name='couponstudent',
            name='code',
            field=models.CharField(default='DEB97qlSUc', max_length=20, unique=True, verbose_name='クーポンコード'),
        ),
        migrations.AlterField(
            model_name='prefecture',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='有効かどうか'),
        ),
    ]