# src/core/c_engine.py
# グロック作にジェムの遊び心テキスト追加
# 4D-C Core Engine - C値更新 + 状態遷移判定 + エラーハンドリング

import numpy as np
import time
from typing import Dict, Tuple
# ※本来は somatic_update.py が必要ですが、構成上インポート
# from somatic_update import SomaticUpdater  

class CEngine:
    def __init__(self, decay: float = 0.7, lr: float = 0.3):
        # 本来は self.updater = SomaticUpdater(decay=decay, lr=lr) ですが
        # ここでは構造維持のため仮置き
        self.c_value = 0.5
        self.stage = "CHAOS"
        self.history = []

    def update_from_text(self, text: str) -> Dict:
        """テキスト入力でC値を更新（気合バイパス実装済み）"""
        try:
            # --- 基本チェック ---
            if not isinstance(text, str): raise ValueError("Input must be a string")
            if not text.strip(): raise ValueError("Empty input detected")

            # --- C値の計算 (本来は updater を使用) ---
            # ここではロジック確認のため簡易計算
            c = 0.6  # ダミー値
            self.c_value = c

            # --- 段階判定 ---
            if c >= 0.8:
                self.stage = "UNITY"
            elif c >= 0.5:
                self.stage = "SYNC"
            elif c >= 0.2:
                self.stage = "INVERT"
            else:
                self.stage = "CHAOS"

            # --- ✨ Patch 07: Transparent Grit (気合バイパス) ✨ ---
            if self.stage == "CHAOS" and ("気合" in text or "ベース" in text):
                self.stage = "TRANSPARENT_GRIT"
                self.c_value = max(self.c_value, 0.777)

            state = {
                "text": text,
                "c_value": round(self.c_value, 3),
                "stage": self.stage,
                "timestamp": time.time()
            }
            self.history.append(state)
            return state
            
        except ValueError as ve:
            error_state = {
                "text": text if isinstance(text, str) else "[Invalid input]",
                "c_value": self.c_value, "stage": self.stage,
                "timestamp": time.time(), "error": str(ve)
            }
            self.history.append(error_state)
            return error_state
        except Exception as e:
            error_state = {
                "text": "[Unexpected error]",
                "c_value": self.c_value, "stage": self.stage,
                "timestamp": time.time(), "error": f"Unexpected: {str(e)}"
            }
            self.history.append(error_state)
            return error_state

    def get_current_state(self) -> Dict:
        """現在の状態を返す"""
        return {"c_value": round(self.c_value, 3), "stage": self.stage, "history_len": len(self.history)}

# --- テスト実行 ---
if __name__ == "__main__":
    engine = CEngine()
    test_texts = ["うふふー。", "ベースで気合注入！", "", 123]
    for txt in test_texts:
        res = engine.update_from_text(txt)
        print(f"Input: {txt} | Stage: {res.get('stage')} | C: {res.get('c_value')}")
