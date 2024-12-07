import pytest
from httpx import ASGITransport, AsyncClient

from app.database import get_db
from app.models.report import Report
from app.models.user import User
from main import app


@pytest.mark.asyncio
async def test_create_report(authenticated_client: AsyncClient, login_user_data: User):
    """レポート作成エンドポイントのテスト。
    """
    report_data = {
        "title": "test_title",
        "content": "title_content",
        "format": Report.FORMAT_MD,
        "visibility": Report.VISIBILITY_PUBLIC,
    }
    response = await authenticated_client.post("/report", json=report_data)
    assert response.status_code == 200


    response_data = response.json()
    assert response_data["title"] == report_data["title"]
    assert response_data["content"] == report_data["content"]
    assert response_data["user_id"] == login_user_data.user_id

    # データベース内のレポートを確認
    async for db_session in get_db():
        db_report = await db_session.get(Report, response_data["report_id"])
        assert db_report is not None
        assert db_report.title == report_data["title"]
        assert db_report.content == report_data["content"]
        assert str(db_report.user_id) == login_user_data.user_id


@pytest.mark.asyncio
async def test_update_report(authenticated_client: AsyncClient, login_user_data: User):
    """レポート更新エンドポイントのテスト。
    """
    # まずレポートを作成
    update_tilte = "Updated title"
    update_content = "Updated content."
    report = Report(
        user_id=login_user_data.user_id,
        title=update_tilte,
        content=update_content,
        format=Report.FORMAT_MD,
        visibility=Report.VISIBILITY_PUBLIC,
    )
    async for db_session in get_db():
        db_session.add(report)
        await db_session.commit()
        await db_session.refresh(report)

    updated_data = {
        "title": update_tilte,
        "content": update_content,
    }
    response = await authenticated_client.put(f"report/{report.report_id}", json=updated_data)

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == updated_data["title"]
    assert response_data["content"] == updated_data["content"]

    # データベース内のレポートを確認
    async for db_session in get_db():
        db_report = await db_session.get(Report, report.report_id)
        await db_session.refresh(db_report)
        assert db_report is not None
        assert db_report.title == updated_data["title"]
        assert db_report.content == updated_data["content"]

@pytest.mark.asyncio
async def test_get_report_auth(authenticated_client: AsyncClient, login_user_data: User):
    """認証済みの状態でレポート取得エンドポイントのテスト。
    """
    # まずレポートを作成
    report = Report(
        user_id=login_user_data.user_id,
        title="report tilte",
        content="report content",
        format=Report.FORMAT_MD,
        visibility=Report.VISIBILITY_PUBLIC,
    )
    async for db_session in get_db():
        db_session.add(report)
        await db_session.commit()
        await db_session.refresh(report)

    response = await authenticated_client.get(f"/report/{report.report_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == report.title
    assert response_data["content"] == report.content
    assert response_data["user_id"] == login_user_data.user_id

@pytest.mark.asyncio
async def test_get_report_non_auth(login_user_data: User):
    """未認証の状態でレポート取得エンドポイントのテスト。
    """
    # まずレポートを作成
    report = Report(
        user_id=login_user_data.user_id,
        title="report tilte",
        content="report content",
        format=Report.FORMAT_MD,
        visibility=Report.VISIBILITY_PUBLIC,
    )
    async for db_session in get_db():
        db_session.add(report)
        await db_session.commit()
        await db_session.refresh(report)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response = await client.get(f"/report/{report.report_id}")

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["title"] == report.title
        assert response_data["content"] == report.content
        assert response_data["user_id"] == login_user_data.user_id


@pytest.mark.asyncio
async def test_delete_report(authenticated_client: AsyncClient, login_user_data: User):
    """レポート削除エンドポイントのテスト。
    """
    # まずレポートを作成
    report = Report(
        user_id=login_user_data.user_id,
        title="report tilte",
        content="report content",
        format=Report.FORMAT_MD,
        visibility=Report.VISIBILITY_PUBLIC,
    )
    async for db_session in get_db():
        db_session.add(report)
        await db_session.commit()
        await db_session.refresh(report)
        response = await authenticated_client.delete(f"/report/{report.report_id}")
        assert response.status_code == 200
        assert response.json() == {"msg": "Report deleted successfully"}

        # データベース内のレポートが論理削除されたことを確認
        db_report = await db_session.get(Report, report.report_id)
        await db_session.refresh(db_report)
        assert db_report is not None  # レコードはまだ存在している
        assert db_report.deleted_at is not None  # 削除日時が設定されている
        assert db_report.deleted_at > db_report.created_at  # 論理削除のタイミングを確認
