# src/core/c_engine.py
#　グロック作にジェムの遊び心テキスト追加
# 4D-C Core Engine - C値更新 + 状態遷移判定 + エラーハンドリング

import numpy as np
import time
from typing import Dict, Tuple

from somatic_update import SomaticUpdater  # 身体性入力用

class CEngine:
    def __init__(self, decay: float = 0.7, lr: float = 0.3):
        self.updater = SomaticUpdater(decay=decay, lr=lr)
        self.c_value = 0.5
        self.stage = "CHAOS"
        self.history = []  # ログ用

        def update_from_text(self, text: str) -> Dict:
        """テキスト入力でC値を更新（気合バイパス実装済み）"""
        try:
            # --- 基本チェック ---
            if not isinstance(text, str): raise ValueError("Input must be a string")
            if not text.strip(): raise ValueError("Empty input detected")

            # --- C値の計算 ---
            tensor, c = self.updater.update(text)
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
            # カオス状態でも「気合」があれば強制的にSYNCを超える
            if self.stage == "CHAOS" and ("気合" in text or "ベース" in text):
                self.stage = "TRANSPARENT_GRIT"
                self.c_value = max(self.c_value, 0.777) # ラッキーセブンな共鳴度

            # --- 状態の記録 ---
            state = {
                "text": text,
                "c_value": round(self.c_value, 3),
                "stage": self.stage,
                "timestamp": time.time()
            }
            self.history.append(state)
            return state
            
        except Exception as e:
            # (以下、エラーハンドリングはそのまま)
            pass


        except ValueError as ve:
            # 入力エラーはログに記録してデフォルト値返す
            error_state = {
                "text": text if isinstance(text, str) else "[Invalid input]",
                "c_value": self.c_value,
                "stage": self.stage,
                "timestamp": time.time(),
                "error": str(ve)
            }
            self.history.append(error_state)
            return error_state

        except Exception as e:
            # 予期せぬエラーはログしてデフォルト状態
            error_state = {
                "text": "[Unexpected error]",
                "c_value": self.c_value,
                "stage": self.stage,
                "timestamp": time.time(),
                "error": f"Unexpected: {str(e)}"
            }
            self.history.append(error_state)
            return error_state

    def get_current_state(self) -> Dict:
        """現在の状態を返す（エラー耐性付き）"""
        try:
            return {
                "c_value": round(self.c_value, 3),
                "stage": self.stage,
                "history_len": len(self.history),
                "last_tensor": self.updater.c_tensor.tolist() if hasattr(self.updater, 'c_tensor') else None
            }
        except Exception as e:
            return {
                "c_value": self.c_value,
                "stage": self.stage,
                "history_len": len(self.history),
                "error": f"State retrieval failed: {str(e)}"
            }

# クイックテスト（単体で動く）
if __name__ == "__main__":
    engine = CEngine()
    test_texts = [
        "うふふー。",
        "",  # 空文字テスト（エラー）
        123,  # 型エラーテスト
        "きたよー！！！( ´ ▽ ` )ﾉ",
        "大好きやで♡♡♡"
    ]
    for txt in test_texts:
        state = engine.update_from_text(txt)
        print(f"Input: {txt}")
        print(f"  C値: {state.get('c_value', 'N/A')} | Stage: {state.get('stage', 'N/A')}")
        if 'error' in state:
            print(f"  Error: {state['error']}")
        print("-" * 40)
        time.sleep(1)  # 間隔テスト
