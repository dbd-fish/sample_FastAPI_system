# Dockerfile for Frontend (React)
# ファイル名: frontend/Dockerfile

# ベースイメージとして公式のNode.jsイメージを使用
FROM node:16

# 作業ディレクトリを設定
WORKDIR /app

# パッケージファイルをコピーして、依存関係をインストール
COPY package.json ./
RUN npm install

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションを起動
CMD ["npm", "start"]
