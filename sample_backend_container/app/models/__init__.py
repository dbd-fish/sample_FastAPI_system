# app/models/__init__.py

# 各モデルをインポート
from .sample_model import SampleModel
from .sample_model2 import SampleModel2
from .sample_model3 import SampleModel3
# 他のモデルがある場合も同様に追加
# from .other_model import OtherModel

# Alembicや他のスクリプトがapp.modelsをインポートするだけで全モデルを認識できるようにする
__all__ = [
    "SampleModel",
    "SampleModel2",
    "SampleModel3",
    # "OtherModel"  # 他のモデルを追加する場合もここに名前を追加
]
