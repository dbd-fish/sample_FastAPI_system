from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReportBase(BaseModel):
    """レポートの基本情報を管理する共通のPydanticモデル。
    リクエスト・レスポンスで共通のフィールドを定義。
    """

    title: str = Field(..., description="レポートのタイトル")
    content: str | None = Field(None, description="レポートの本文")
    format: int = Field(1, description="フォーマット (1: md, 2: html)")
    visibility: int = Field(3, description="公開設定 (1: public, 2: group, 3: private)")

class RequestReport(ReportBase):
    """リクエストデータ専用のモデル。
    """

    # 拡張用

class ResponseReport(ReportBase):
    """レスポンスデータ専用のモデル。
    レポートのIDやタイムスタンプなど、レスポンス時に必要なフィールドを追加。
    """

    report_id: UUID = Field(..., description="レポートの一意な識別子")
    user_id: UUID = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    deleted_at: datetime | None = Field(None, description="削除日時")

    model_config = ConfigDict(from_attributes = True)
