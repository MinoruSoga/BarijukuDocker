# Pythonのベースイメージを指定
FROM python:3.10.9

# 作業ディレクトリを指定
WORKDIR /usr/src/app

# 依存関係のインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトコードのコピー
COPY . .

# 静的ファイルの収集
RUN python manage.py collectstatic --noinput

# Gunicornを起動
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
