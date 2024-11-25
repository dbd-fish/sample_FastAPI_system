# Dockerfile for Backend (Django)
# ファイル名: backend/Dockerfile

# ベースイメージとして公式のPythonイメージを使用
FROM python:3.13

# 作業ディレクトリを設定
WORKDIR /app
ENV PYTHONUNBUFFERED 1

# poetryインストール
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry


# コンテナ内で仮想環境の作成を無効
RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project true

COPY . .

# 依存関係をインストール
RUN poetry install --no-interaction

# 環境変数の設定
ENV PATH="/root/.local/bin:${PATH}"
# PYTHONPATHを設定
ENV PYTHONPATH="/app" 



