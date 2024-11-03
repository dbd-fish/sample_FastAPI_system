
-- ユーザー管理テーブル (User Management)

CREATE TABLE user (
    user_id INT PRIMARY KEY COMMENT 'ユーザーID',
    username VARCHAR(50) NOT NULL COMMENT 'ユーザー名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'メールアドレス',
    password_hash VARCHAR(255) NOT NULL COMMENT 'パスワード（ハッシュ）',
    role ENUM('guest', 'free', 'regular', 'admin', 'owner') NOT NULL COMMENT 'ユーザー権限',
    status ENUM('active', 'suspended') NOT NULL COMMENT 'アカウント状態',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時'
) COMMENT='ユーザー';

-- ユーザーのIPアドレスを管理するテーブル
CREATE TABLE user_ip_address (
    ip_id INT PRIMARY KEY COMMENT 'IP ID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    ip_address VARCHAR(45) NOT NULL COMMENT 'IPアドレス',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
) COMMENT='ユーザーごとのIPアドレス';

CREATE TABLE user_group (
    group_id INT PRIMARY KEY COMMENT 'グループID',
    group_name VARCHAR(50) UNIQUE NOT NULL COMMENT 'グループ名',
    parent_group_id INT NULL COMMENT '親グループID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (parent_group_id) REFERENCES user_group(group_id)
) COMMENT='グループ';

CREATE TABLE user_group_membership (
    user_id INT NOT NULL COMMENT 'ユーザーID',
    group_id INT NOT NULL COMMENT 'グループID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (group_id) REFERENCES user_group(group_id)
) COMMENT='ユーザーとグループの関連';

-- レポート管理テーブル (Report Management)

CREATE TABLE report (
    report_id INT PRIMARY KEY COMMENT 'レポートID',
    user_id INT NOT NULL COMMENT '作成者ユーザーID',
    title VARCHAR(100) NOT NULL COMMENT 'タイトル',
    content TEXT COMMENT '内容',
    format ENUM('md', 'html') DEFAULT 'md' COMMENT 'フォーマット',
    visibility ENUM('public', 'group', 'private') DEFAULT 'private' COMMENT '公開設定',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='レポート';

CREATE TABLE report_tag (
    tag_id INT PRIMARY KEY COMMENT 'タグID',
    tag_name VARCHAR(50) UNIQUE NOT NULL COMMENT 'タグ名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時'
) COMMENT='タグ';

CREATE TABLE report_tag_link (
    report_id INT NOT NULL COMMENT 'レポートID',
    tag_id INT NOT NULL COMMENT 'タグID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    PRIMARY KEY (report_id, tag_id),
    FOREIGN KEY (report_id) REFERENCES report(report_id),
    FOREIGN KEY (tag_id) REFERENCES report_tag(tag_id)
) COMMENT='レポートとタグの関連';

CREATE TABLE report_comment (
    comment_id INT PRIMARY KEY COMMENT 'コメントID',
    report_id INT NOT NULL COMMENT 'レポートID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    content TEXT COMMENT 'コメント内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (report_id) REFERENCES report(report_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='レポートのコメント';

-- 評価テーブル (Evaluation Tables)

CREATE TABLE user_evaluation (
    eval_id INT PRIMARY KEY COMMENT '評価ID',
    evaluator_id INT NOT NULL COMMENT '評価者ID',
    evaluatee_id INT NOT NULL COMMENT '被評価者ID',
    score INT CHECK(score BETWEEN 0 AND 100) COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (evaluator_id) REFERENCES user(user_id),
    FOREIGN KEY (evaluatee_id) REFERENCES user(user_id)
) COMMENT='ユーザー評価';

CREATE TABLE group_evaluation (
    eval_id INT PRIMARY KEY COMMENT '評価ID',
    evaluator_id INT NOT NULL COMMENT '評価者ID',
    group_id INT NOT NULL COMMENT 'グループID',
    score INT CHECK(score BETWEEN 0 AND 100) COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (evaluator_id) REFERENCES user(user_id),
    FOREIGN KEY (group_id) REFERENCES user_group(group_id)
) COMMENT='グループ評価';

-- 履歴テーブル (History Tables)

CREATE TABLE report_view_history (
    history_id INT PRIMARY KEY COMMENT '履歴ID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    report_id INT NOT NULL COMMENT 'レポートID',
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '閲覧日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (report_id) REFERENCES report(report_id)
) COMMENT='レポート閲覧履歴';

CREATE TABLE user_view_history (
    history_id INT PRIMARY KEY COMMENT '履歴ID',
    viewer_id INT NOT NULL COMMENT '閲覧者ID',
    viewed_user_id INT NOT NULL COMMENT '閲覧対象ユーザーID',
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '閲覧日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (viewer_id) REFERENCES user(user_id),
    FOREIGN KEY (viewed_user_id) REFERENCES user(user_id)
) COMMENT='ユーザー閲覧履歴';

-- 検索テーブル (Search Tables)

CREATE TABLE user_search_history (
    search_id INT PRIMARY KEY COMMENT '検索ID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    search_term VARCHAR(100) COMMENT '検索キーワード',
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '検索日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='ユーザー検索履歴';

CREATE TABLE group_search_history (
    search_id INT PRIMARY KEY COMMENT '検索ID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    search_term VARCHAR(100) COMMENT '検索キーワード',
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '検索日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='グループ検索履歴';
