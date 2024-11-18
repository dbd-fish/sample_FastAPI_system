# app/common/common.py
from datetime import datetime
from zoneinfo import ZoneInfo

# def datetime_now():
#     """
#     日本時間（Asia/Tokyo）の現在時刻を取得し、フォーマットする。
#     フォーマット例: 2024-11-17 14:46:22.127
#     """
#     return datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
def datetime_now():
    """
    日本時間（Asia/Tokyo）の現在時刻を取得する。
    """
    print(datetime.now(ZoneInfo("Asia/Tokyo")).replace(microsecond=0))
    return datetime.now(ZoneInfo("Asia/Tokyo")).replace(tzinfo=None, microsecond=0)