# import pytest
# from httpx import AsyncClient
# from main import app
# from app.core.security import create_access_token
# from app.models.user import User
# from app.models.report import Report
# from app.database import Base, engine
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.schemas.report import RequestReport

# @pytest.fixture(autouse=True)
# async def setup_db():
#     """
#     テスト用のデータベースをセットアップします。
#     """
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture
# async def test_user():
#     """
#     テスト用のユーザーをデータベースに追加します。
#     """
#     async with AsyncSession(engine) as session:
#         user = User(
#             email="testuser@example.com",
#             username="testuser",
#             password_hash="hashedpassword",
#             user_status=1
#         )
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#         return user

# @pytest.fixture
# def access_token(test_user):
#     """
#     テスト用のアクセストークンを生成します。
#     """
#     return create_access_token({"sub": test_user.email})

# @pytest.mark.anyio
# async def test_create_report(test_user, access_token):
#     """
#     レポート作成のテスト。
#     """
#     report_data = {
#         "title": "Test Report",
#         "content": "This is a test report.",
#         "format": 1,
#         "visibility": 3
#     }
#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.post(
#             "/reports", json=report_data, headers={"Authorization": f"Bearer {access_token}"}
#         )
#         assert response.status_code == 200
#         assert response.json()["title"] == report_data["title"]

# @pytest.mark.anyio
# async def test_get_report(test_user, access_token):
#     """
#     レポート取得のテスト。
#     """
#     async with AsyncSession(engine) as session:
#         report = Report(
#             user_id=test_user.user_id,
#             title="Existing Report",
#             content="Existing content",
#             format=1,
#             visibility=3
#         )
#         session.add(report)
#         await session.commit()
#         await session.refresh(report)

#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.get(
#             f"/reports/{str(report.report_id)}", headers={"Authorization": f"Bearer {access_token}"}
#         )
#         assert response.status_code == 200
#         assert response.json()["title"] == "Existing Report"

# @pytest.mark.anyio
# async def test_update_report(test_user, access_token):
#     """
#     レポート更新のテスト。
#     """
#     async with AsyncSession(engine) as session:
#         report = Report(
#             user_id=test_user.user_id,
#             title="Old Report",
#             content="Old content",
#             format=1,
#             visibility=3
#         )
#         session.add(report)
#         await session.commit()
#         await session.refresh(report)

#     updated_data = {
#         "title": "Updated Report",
#         "content": "Updated content",
#         "format": 2,
#         "visibility": 1
#     }

#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.put(
#             f"/reports/{str(report.report_id)}",
#             json=updated_data,
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         assert response.status_code == 200
#         assert response.json()["title"] == "Updated Report"

# @pytest.mark.anyio
# async def test_delete_report(test_user, access_token):
#     """
#     レポート削除のテスト。
#     """
#     async with AsyncSession(engine) as session:
#         report = Report(
#             user_id=test_user.user_id,
#             title="Report to delete",
#             content="Delete content",
#             format=1,
#             visibility=3
#         )
#         session.add(report)
#         await session.commit()
#         await session.refresh(report)

#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.delete(
#             f"/reports/{str(report.report_id)}",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         assert response.status_code == 200
#         assert response.json()["message"] == "Report deleted successfully"
