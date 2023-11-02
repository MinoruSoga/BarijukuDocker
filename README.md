## django doc
https://docs.djangoproject.com/ja/4.1/

## カレンダー
https://mdbootstrap.com/docs/standard/plugins/calendar/
https://blog.narito.ninja/detail/160

## 起動
$ source myvenv/bin/activate
(myvenv)$ python manage.py runserver
http://127.0.0.1:8000/　ブラウザにてアクセス

## スーパーユーザー作成

## マスタデータ登録
(myvenv)$ python manage.py loaddata app/fixtures/prefecture-data.json
(myvenv)$ python manage.py loaddata app/fixtures/city-data.json

## Stripe CLI　をインストール
$ brew install stripe/stripe-cli/stripe

$ stripe listen --forward-to localhost:8000/student/stripe/webhook/
- レスポンスのWEBHOOKシークレットキーをenvファイルに登録
^^^
Your webhook signing secret is 'xxxxx WEBHOOKシークレットキーxxxxxx' (^C to quit)
# StripeのWebhookのシークレットキー
STRIPE_WEBHOOK_SECRET = 'ここにSTRIPE_WEBHOOK_SECRETを入力'
^^^


# ダンプデータ
$ python manage.py loaddata app/fixtures/data.json
$ python manage.py loaddata student/fixtures/data.json


# Docker
$ docker-compose up --build
$ docker-compose up -d
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate

$ docker cp barijuku_db.sql barijuku_db:/barijuku_db.sql

$ docker-compose exec db bash

$ mysql -u root -p barijuku_db < /barijuku_db.sql
>password


ブラウザで「http://localhost/」にアクセス