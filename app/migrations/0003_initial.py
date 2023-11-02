# Generated by Django 4.1.7 on 2023-05-07 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('app', '0002_initial'),
        ('student', '0001_initial'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingschedule',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.trainer'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.meetingschedule'),
        ),
        migrations.AddField(
            model_name='couponstudent',
            name='coupon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.coupon'),
        ),
        migrations.AddField(
            model_name='couponstudent',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop'),
        ),
        migrations.AddField(
            model_name='couponstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AddField(
            model_name='city',
            name='prefecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.prefecture'),
        ),
        migrations.AddField(
            model_name='chatgptlog',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.place'),
        ),
    ]