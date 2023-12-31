# Generated by Django 4.1.7 on 2023-05-07 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='開始日時')),
                ('end_date', models.DateTimeField(verbose_name='終了日時')),
                ('is_student', models.IntegerField(default=1)),
                ('content', models.CharField(max_length=50, null=True, verbose_name='内容')),
            ],
        ),
        migrations.CreateModel(
            name='ChatGPTLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_content', models.TextField(null=True, verbose_name='リクエスト内容')),
                ('response_content', models.TextField(null=True, verbose_name='レスポンス内容')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='市町村')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効かどうか')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True, verbose_name='クーポン名')),
                ('type', models.CharField(max_length=50, null=True, verbose_name='クーポンタイプ')),
                ('price', models.IntegerField(default=1000)),
                ('is_active', models.BooleanField(default=True, verbose_name='有効かどうか')),
            ],
        ),
        migrations.CreateModel(
            name='CouponStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='MIITmtgZGM', max_length=20, unique=True, verbose_name='クーポンコード')),
                ('is_used', models.BooleanField(default=False, verbose_name='使用済')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='有効期限')),
                ('used_date', models.DateTimeField(blank=True, null=True, verbose_name='利用日時')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50, null=True, verbose_name='内容')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prefecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefecture', models.CharField(max_length=50, verbose_name='都道府県')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効かどうか')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=50, null=True, verbose_name='名称')),
                ('postal_code', models.CharField(max_length=50, null=True, verbose_name='郵便番号')),
                ('address', models.CharField(max_length=50, null=True, verbose_name='番地以降')),
                ('entry_date', models.DateField(null=True, verbose_name='開校日')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.city')),
                ('prefecture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.prefecture')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='開始日時')),
                ('end_date', models.DateTimeField(verbose_name='終了日時')),
                ('content', models.CharField(max_length=50, null=True, verbose_name='内容')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.place')),
            ],
        ),
    ]
