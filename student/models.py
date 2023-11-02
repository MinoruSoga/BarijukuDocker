from django.db import models

# from django.contrib.auth.models import User
from app.models import Prefecture
from app.models import City

from django.conf import settings

User = settings.AUTH_USER_MODEL


class SchoolCategory(models.Model):
    school_category = models.CharField("小中高", max_length=50)

    def __str__(self):
        return self.school_category


class School(models.Model):
    school = models.CharField("学校名", max_length=50)
    school_category = models.ForeignKey(SchoolCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.school


class ClubActivity(models.Model):
    club_activity = models.CharField("部活動", max_length=50)

    def __str__(self):
        return self.club_activity


class Subject(models.Model):
    subject = models.CharField("教科名", max_length=50)
    grade = models.CharField("学年", max_length=50, null=True, blank=True)
    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    school_category = models.ForeignKey(
        SchoolCategory, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.subject


class TestCategory(models.Model):
    test_category = models.CharField("テストの種類", max_length=50)
    school_category = models.ForeignKey(
        SchoolCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    grade = models.CharField("学年", max_length=50, null=True, blank=True)
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.test_category


class Student(models.Model):
    last_name = models.CharField("生徒 性", max_length=50)
    first_name = models.CharField("生徒 名", max_length=50)
    last_name_kana = models.CharField("生徒 性 カナ", max_length=50)
    first_name_kana = models.CharField("生徒 名 カナ", max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.CharField("学年", max_length=50, null=True, blank=True)
    school_class = models.CharField("組", max_length=50, null=True, blank=True)
    club_activity = models.ForeignKey(
        ClubActivity, on_delete=models.CASCADE, null=True, blank=True
    )
    phone_number = models.CharField("電話番号", max_length=50, null=True, blank=True)
    parent_last_name = models.CharField("保護者 性", max_length=50, null=True, blank=True)
    parent_first_name = models.CharField("保護者 名", max_length=50, null=True, blank=True)
    parent_last_name_kana = models.CharField(
        "保護者 性 カナ", max_length=50, null=True, blank=True
    )
    parent_first_name_kana = models.CharField(
        "保護者 名 カナ", max_length=50, null=True, blank=True
    )
    parent_phone_number = models.CharField(
        "保護者電話番号", max_length=50, null=True, blank=True
    )
    parent_email = models.CharField("保護者 メールアドレス", max_length=50, null=True, blank=True)
    zipcode = models.CharField("郵便番号", max_length=50, null=True, blank=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    address = models.CharField("番地以降", max_length=50, null=True)
    entry_date = models.DateField("入塾日", null=True)
    expiration_date = models.DateField("有効期限", null=True)
    stripe_data = models.CharField("Stripe決済情報", max_length=250, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introducer_last_name = models.CharField(
        "紹介者　性", max_length=50, null=True, blank=True
    )
    introducer_first_name = models.CharField(
        "紹介者　名", max_length=50, null=True, blank=True
    )

    unsubscribe_request = models.BooleanField(verbose_name="退塾申請", default=False)

    def __str__(self):
        return self.last_name


class TestResult(models.Model):
    score = models.CharField("テスト結果", max_length=50, blank=True)
    date = models.DateField("テスト日", null=True, blank=True)
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.score


class AverageTestResult(models.Model):
    score = models.CharField("平均点", max_length=50)
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.score


class AtamaPlus(models.Model):
    login_id = models.CharField("ログインID", max_length=50)
    password = models.CharField("パスワード", max_length=50)
    site_url = models.CharField("サイトURL", max_length=100)
    # user_id = models.ForeignKey(User, verbose_name='AuthUser', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.login_id


class StudySapuri(models.Model):
    login_id = models.CharField("ログインID", max_length=50)
    password = models.CharField("パスワード", max_length=50)
    site_url = models.CharField("サイトURL", max_length=100)
    # user_id = models.ForeignKey(User, verbose_name='AuthUser', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.login_id


class StudentTarget(models.Model):
    content = models.CharField("内容", max_length=100)
    description = models.CharField("詳細", max_length=500, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
