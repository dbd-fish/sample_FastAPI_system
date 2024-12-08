# リポジトリ概要
可能な限り最新の情報(2024年11月時点)を取り入れたFastAPIのサンプルプロジェクト。
Dockerで環境構築しており、フロント(未作成)、バックエンド、DBでコンテナを分けている。
Qiitaのような記事を投稿するシステムをイメージして、一部機能を作成しています。

# 主な技術スタック
- 言語: python 3.13
- フレームワーク: FastAPI (非同期) 0.115.5
- データベース: PostgreSQL 13
- 環境構築: docker-compose.yml, Dockerfile
- パッケージ管理: Poetry 1.8.4
- ORM: SQLAlchemy (非同期) 2.0.36
- マイグレーション: alembic 1.14.0
- 型チェック: mypy 1.13.0
- 静的コード解析: Ruff 0.7.4
- テスト: Pytest 8.3.3, pytest-asyncio
- 非同期サポート: asyncio 0.24.0
- ログ: structlog 24.4.0, logging
- 認証: JWT
- パスワードハッシュ: Passlib

# ディレクトリ構成
下記のようなディレクトリ構成としました。
設計思想としては、MVC+Service+Repositoryを採用しています。
今回はフロント部分を作成していないためViewに当たるディレクトリは未作成です。
```txt
C:.
│  docker-compose.yml              # Docker Composeで複数のコンテナ構成を定義する設定ファイル
│  
├─document                         # プロジェクトに関連するドキュメントを管理するフォルダ
│  │  
│  └─v1                            # ドキュメントのバージョン管理（v1）用フォルダ。実装前の設計案。
│      │  
│      ├─01_要件定義               # 要件定義に関連する資料を管理するフォルダ
│      │     機能一覧.md           # システムで実装する機能一覧を記載
│      │     要件定義書.md         # システム要件の詳細を記載したドキュメント
│      │     
│      │          
│      ├─02_基本設計               # 基本設計に関連する資料を管理するフォルダ
│      │      DB.sql               # データベースの構造を定義したSQLスクリプト。ER図はDbeaverなどから自動生成できるため省略。
│      │      画面遷移図.drawio    # システムの画面遷移図
│      │      開発環境.md          # 開発環境の設定や構成について記載
│            
├─init-scripts                     # 初期化スクリプトを管理するフォルダ
│      create_test_databases.sql   # テスト用のデータベースを作成するSQLスクリプト
│      
├─sample_backend_container         # バックエンドアプリケーションに関連するフォルダ
│  │  alembic.ini                 # Alembic（データベースマイグレーションツール）の設定ファイル
│  │  Dockerfile                  # バックエンド用Dockerイメージのビルド設定
│  │  main.py                     # アプリケーションのエントリーポイント
│  │  poetry.lock                 # Poetryによる依存関係のロックファイル
│  │  pyproject.toml              # Poetryで定義されたプロジェクト情報と依存関係
│  │  
│  ├─.vscode                      # Visual Studio Codeのプロジェクト設定フォルダ
│  │      settings.json           # エディタ設定や拡張機能設定ファイル
│  │      
│  ├─alembic                      # Alembic関連ファイルを管理
│  │  │  env.py                  # マイグレーション環境の設定ファイル
│  │  │  script.py.mako          # マイグレーションスクリプトのテンプレート
│  │  │  
│  │  └─versions                 # データベーススキーマのバージョン管理フォルダ
│  │          79401c48e0d8_recreate_migration.py # 自動生成されるマイグレーションファイル
│  │          
│  ├─app                          # バックエンドアプリケーションの主要コード
│  │  │  database.py             # データベース接続の設定
│  │  │  routes.py               # APIルート設定
│  │  
│  │  ├─common                   # 共通関数や汎用モジュール
│  │  │      common.py           # 汎用ユーティリティ関数
│  │  
│  │  ├─config                   # 設定関連ファイル
│  │  │      setting.py          # アプリケーションの設定を管理
│  │  │      test_data.py        # テスト用の定数定義ファイル
│  │  
│  │  ├─controllers              # コントローラ（APIエンドポイントの処理）
│  │  │      auth_controller.py  # 認証に関連するエンドポイント
│  │  │      dev_controller.py   # 開発者向けAPI
│  │  │      report_controller.py# レポート関連のエンドポイント
│  │  
│  │  ├─core                     # アプリケーションのコア機能
│  │  │      http_exception_handler.py # HTTP例外処理
│  │  │      log_config.py       # ログ設定
│  │  │      request_validation_error.py # リクエスト時のバリデーション例外処理
│  │  │      security.py         # 認証関連の基本となる処理
│  │  
│  │  ├─middleware               # ミドルウェア機能
│  │  │      add_userIP_middleware.py # ユーザーIPアドレス追加ミドルウェア
│  │  │      error_handler_middleware.py # エラーハンドラーミドルウェア
│  │  
│  │  ├─models                   # データベースモデル
│  │  │      report.py                     # レポートデータモデル
│  │  │      user.py                       # ユーザーデータモデル
│  │  │      # 他ファイルの説明は省略

│  │  
│  │  ├─repositories             # データ操作を抽象化したリポジトリ層
│  │  │      auth_repository.py  # 認証情報の操作
│  │  │      report_repository.py# レポートデータ操作
│  │  
│  │  ├─schemas                  # Pydanticを用いたリクエストやレスポンスの型を定義
│  │  │      report.py           # レポート関連のPydaticスキーマ
│  │  │      user.py             # ユーザー関連のPydaticスキーマ
│  │  
│  │  ├─seeders                  # 初期データ投入用スクリプト
│  │  │      seed_data.py        # 初期データの投入処理。ファイル量が膨大になるため、本来はテーブル単位で別ファイル化したほうがよいかも。
│  │  
│  │  └─services                 # ビジネスロジック層
│  │          auth_service.py    # 認証ロジック
│  │          report_service.py  # レポート関連のロジック
│          
├─logs                          # ログ全般を管理するフォルダ
│  ├─Pytest                     # Pytest実行時のログを格納するフォルダ
│  │  ├─app                     # Pytestにおけるアプリケーション動作ログ
│  │  │      app_2024-12-06.log # Pytest実行時のアプリケーション動作ログ（例: 2024年12月6日のログ）
│  │  │      
│  │  └─sql                     # PytestにおけるSQLAlchemyの動作ログ
│  │          sqlalchemy_2024-12-06.log # Pytest実行時のSQLAlchemyログ（例: 2024年12月6日のログ）
│  │          
│  └─Server                     # サーバー運用時のログを格納するフォルダ
│      ├─app                    # サーバー運用時のアプリケーション動作ログ
│      │      app_2024-12-08.log # サーバー運用中のアプリケーション動作ログ（例: 2024年12月8日のログ）
│      │      
│      └─sql                    # サーバー運用時のSQLAlchemyの動作ログ
│              sqlalchemy_2024-12-08.log # サーバー運用中のSQL
│  │  
│  └─tests                       # pytestコード
│      │  conftest.py            # テスト共通設定。本ファイルでフィクスチャを読み込んでいる。
│      ├─fixtures                # テストデータや設定用フィクスチャ
│      │      authenticate_fixture.py # 認証関連のテストフィクスチャ
│      │      db_fixture.py      # データベース関連のテストフィクスチャ
│      │      logging_fixture.py # ログ関連のテストフィクスチャ
│      ├─integration             # 統合テストコード
│      │      test_auth_controller.py # 認証エンドポイントの統合テスト
│      │      test_report_controller.py # レポートエンドポイントの統合テスト
│      └─unit                    # 単体テストコード
│          └─core
│                  test_security.py # セキュリティ関連の単体テスト
│                  
└─sample_frontend_container       # フロントエンド用のコンテナ設定（今後作成予定）
        Dockerfile                # フロントエンド用Dockerビルド設定（今後作成予定）
```

# 環境構築手順
Docker環境を構築して下記コマンドを実行。
```Bash
docker-compose up --build
```

下記URLからAPIの動作確認が可能。  
http://localhost:8000/docs

# 各種コマンド
コンテナ内で下記コマンドを実行可能。


## Pytest
下記コマンドPytestを実行可能。
```Bash
poetry run pytest
```

## Ruff
下記コマンドで静的コード解析＆自動修正。
```Bash
poetry run ruff check . --fix
```

## mypy
下記コマンドで型チェック。
```Bash
poetry run mypy .
```

## alembic
下記記事にまとめています。  
https://qiita.com/dbd_fish/items/39f74e7c4c699cc724c3

# 今後の展望
- Github Actionの導入
- フロントの作成
- Warnig以上のログを別ファイル化
- 単体テストの充実化(mockを利用する)
