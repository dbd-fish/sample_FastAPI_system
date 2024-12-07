# app/models/__init__.py

# 各モデルをインポート
from .group_evaluation import GroupEvaluation
from .group_evaluation_history import GroupEvaluationHistory
from .group_profile import GroupProfile
from .group_search_history import GroupSearchHistory
from .report import Report
from .report_comment_history import ReportCommentHistory
from .report_evaluation_history import ReportEvaluationHistory
from .report_supplement import ReportSupplement
from .report_tag import ReportTag
from .report_tag_link import ReportTagLink
from .report_view_history import ReportViewHistory
from .tag_view_history import TagViewHistory
from .user import User
from .user_evaluation_history import UserEvaluationHistory
from .user_group import UserGroup
from .user_group_membership import UserGroupMembership
from .user_ip_address import UserIPAddress
from .user_profile import UserProfile
from .user_search_history import UserSearchHistory
from .user_view_history import UserViewHistory

# 他のモデルがある場合も同様に追加
# from .other_model import OtherModel

# Alembicや他のスクリプトがapp.modelsをインポートするだけで全モデルを認識できるようにする
__all__ = [
    "user",
    "user_profile",
    "user_ip_address",
    "user_group",
    "group_profile",
    "user_group_membership",
    "report",
    "report_tag",
    "report_tag_link",
    "report_supplement",
    "user_evaluation_history",
    "report_evaluation_history",
    "group_evaluation_history",
    "report_comment_history",
    "tag_view_history",
    "group_evaluation",
    "report_view_history",
    "user_view_history",
    "user_search_history",
    "group_search_history",
    # "OtherModel"  # 他のモデルを追加する場合もここに名前を追加
]
