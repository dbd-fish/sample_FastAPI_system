-- ユーザー管理テーブル (User Management)
CREATE TABLE user (
    user_id CHAR(36) PRIMARY KEY COMMENT 'ユーザーID (UUID)',
    username VARCHAR(50) NOT NULL COMMENT 'ユーザー名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'メールアドレス',
    password_hash VARCHAR(255) NOT NULL COMMENT 'パスワード（ハッシュ）',
    role TINYINT NOT NULL COMMENT 'ユーザー権限 (1: guest, 2: free, 3: regular, 4: admin, 5: owner)',
    status TINYINT NOT NULL COMMENT 'アカウント状態 (1: active, 2: suspended)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時'
) COMMENT='ユーザー';

-- ユーザーのIPアドレスを管理するテーブル
CREATE TABLE user_ip_address (
    ip_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'IP ID',
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    ip_address VARCHAR(45) NOT NULL COMMENT 'IPアドレス',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
) COMMENT='ユーザーごとのIPアドレス';

-- グループ管理テーブル
CREATE TABLE user_group (
    group_id CHAR(36) PRIMARY KEY COMMENT 'グループID (UUID)',
    group_name VARCHAR(50) UNIQUE NOT NULL COMMENT 'グループ名',
    parent_group_id CHAR(36) NULL COMMENT '親グループID (UUID)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (parent_group_id) REFERENCES user_group(group_id)
) COMMENT='グループ';

CREATE TABLE user_group_membership (
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    group_id CHAR(36) NOT NULL COMMENT 'グループID (UUID)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (group_id) REFERENCES user_group(group_id)
) COMMENT='ユーザーとグループの関連';

-- レポート管理テーブル (Report Management)
CREATE TABLE report (
    report_id CHAR(36) PRIMARY KEY COMMENT 'レポートID (UUID)',
    user_id CHAR(36) NOT NULL COMMENT '作成者ユーザーID (UUID)',
    title VARCHAR(100) NOT NULL COMMENT 'タイトル',
    content TEXT COMMENT '内容',
    format TINYINT NOT NULL DEFAULT 1 COMMENT 'フォーマット (1: md, 2: html)',
    visibility TINYINT NOT NULL DEFAULT 3 COMMENT '公開設定 (1: public, 2: group, 3: private)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='レポート';

-- タグ管理テーブル
CREATE TABLE report_tag (
    tag_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'タグID',
    tag_name VARCHAR(50) UNIQUE NOT NULL COMMENT 'タグ名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時'
) COMMENT='タグ';

CREATE TABLE report_tag_link (
    report_id CHAR(36) NOT NULL COMMENT 'レポートID (UUID)',
    tag_id INT NOT NULL COMMENT 'タグID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    PRIMARY KEY (report_id, tag_id),
    FOREIGN KEY (report_id) REFERENCES report(report_id),
    FOREIGN KEY (tag_id) REFERENCES report_tag(tag_id)
) COMMENT='レポートとタグの関連';

-- レポートコメントテーブル
CREATE TABLE report_comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'コメントID',
    report_id CHAR(36) NOT NULL COMMENT 'レポートID (UUID)',
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    content TEXT COMMENT 'コメント内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (report_id) REFERENCES report(report_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='レポートのコメント';

-- ユーザー評価テーブル (Evaluation Tables)
CREATE TABLE user_evaluation (
    eval_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '評価ID',
    evaluator_id CHAR(36) NOT NULL COMMENT '評価者ID (UUID)',
    evaluatee_id CHAR(36) NOT NULL COMMENT '被評価者ID (UUID)',
    score INT CHECK(score BETWEEN 0 AND 100) COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (evaluator_id) REFERENCES user(user_id),
    FOREIGN KEY (evaluatee_id) REFERENCES user(user_id)
) COMMENT='ユーザー評価';

CREATE TABLE report_evaluation_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '評価履歴ID',
    eval_id INT NOT NULL COMMENT '評価ID',
    user_id CHAR(36) NOT NULL COMMENT '評価者ユーザーID (UUID)',
    report_id CHAR(36) NOT NULL COMMENT 'レポートID (UUID)',
    score INT COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    FOREIGN KEY (eval_id) REFERENCES report_evaluation(eval_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (report_id) REFERENCES report(report_id)
) COMMENT='レポート評価履歴';

CREATE TABLE group_evaluation_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '評価履歴ID',
    eval_id INT NOT NULL COMMENT '評価ID',
    user_id CHAR(36) NOT NULL COMMENT '評価者ユーザーID (UUID)',
    group_id CHAR(36) NOT NULL COMMENT 'グループID (UUID)',
    score INT COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    FOREIGN KEY (eval_id) REFERENCES group_evaluation(eval_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (group_id) REFERENCES user_group(group_id)
) COMMENT='グループ評価履歴';

CREATE TABLE report_comment_evaluation_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '評価履歴ID',
    eval_id INT NOT NULL COMMENT '評価ID',
    user_id CHAR(36) NOT NULL COMMENT '評価者ユーザーID (UUID)',
    comment_id INT NOT NULL COMMENT 'コメントID',
    score INT COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    FOREIGN KEY (eval_id) REFERENCES report_comment_evaluation(eval_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (comment_id) REFERENCES report_comment(comment_id)
) COMMENT='コメント評価履歴';

CREATE TABLE group_evaluation (
    eval_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '評価ID',
    evaluator_id CHAR(36) NOT NULL COMMENT '評価者ID (UUID)',
    group_id CHAR(36) NOT NULL COMMENT 'グループID (UUID)',
    score INT CHECK(score BETWEEN 0 AND 100) COMMENT '評価スコア',
    comment TEXT COMMENT '評価コメント',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (evaluator_id) REFERENCES user(user_id),
    FOREIGN KEY (group_id) REFERENCES user_group(group_id)
) COMMENT='グループ評価';

-- 履歴テーブル (History Tables)
CREATE TABLE report_view_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '履歴ID',
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    report_id CHAR(36) NOT NULL COMMENT 'レポートID (UUID)',
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '閲覧日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (report_id) REFERENCES report(report_id)
) COMMENT='レポート閲覧履歴';

CREATE TABLE user_view_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '履歴ID',
    viewer_id CHAR(36) NOT NULL COMMENT '閲覧者ID (UUID)',
    viewed_user_id CHAR(36) NOT NULL COMMENT '閲覧対象ユーザーID (UUID)',
    view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '閲覧日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (viewer_id) REFERENCES user(user_id),
    FOREIGN KEY (viewed_user_id) REFERENCES user(user_id)
) COMMENT='ユーザー閲覧履歴';

-- 検索テーブル (Search Tables)
CREATE TABLE user_search_history (
    search_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '検索ID',
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    search_term VARCHAR(100) COMMENT '検索キーワード',
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '検索日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='ユーザー検索履歴';

CREATE TABLE group_search_history (
    search_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '検索ID',
    user_id CHAR(36) NOT NULL COMMENT 'ユーザーID (UUID)',
    search_term VARCHAR(100) COMMENT '検索キーワード',
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '検索日時',
    deleted_at TIMESTAMP NULL COMMENT '削除日時',
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) COMMENT='グループ検索履歴';
