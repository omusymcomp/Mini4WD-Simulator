import json
import os
import sys

try:
    # Unreal Engine環境でのみ実行されるため、unrealモジュールが必須
    import unreal
except ImportError:
    print("🚨 エラー: unrealモジュールが見つかりません。このスクリプトはUnreal EngineエディタのPythonコンソールで実行してください。")
    sys.exit(1)

# --- 設定 ---

# JSONファイルが保存されているディレクトリのパス
BASE_DIR = r"C:\Users\takumi\Documents\Mini4WD-Simulator\Content\Python"

# 🎯 上書き対象となる単一のCurveFloatアセットのパス
TARGET_CURVE_ASSET_PATH = "/Game/BluePrints/Vheicle/HyperDash_M"

# 検索対象となる RichCurve プロパティ名のリスト (可能性の高い順に試行)
RICH_CURVE_PROPERTY_NAMES = [
    "float_curve",      # 新規作成時に有効だった名前
    "FloatCurve",       # C++名
    "CurveData",        # その他の可能性
]

# --- Enum の対応表 (共通設定) ---
INTERP_MODE_MAP = {
    "RCIM_Linear": unreal.RichCurveInterpMode.RCIM_LINEAR, "RCIM_Constant": unreal.RichCurveInterpMode.RCIM_CONSTANT, "RCIM_Cubic": unreal.RichCurveInterpMode.RCIM_CUBIC,
}
TANGENT_MODE_MAP = {
    "RCTM_Auto": unreal.RichCurveTangentMode.RCTM_AUTO, "RCTM_User": unreal.RichCurveTangentMode.RCTM_USER, "RCTM_Break": unreal.RichCurveTangentMode.RCTM_BREAK,
}
TANGENT_WEIGHT_MODE_MAP = {
    "RCTWM_WeightedNone": unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_NONE, 
    "RCTWM_WeightedArrive": unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_ARRIVE, 
    "RCTWM_WeightedLeave": unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_LEAVE, 
    "RCTWM_WeightedBoth": unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_BOTH,
}
EXTRAP_MAP = {
    "RCCE_Constant": unreal.RichCurveExtrapolation.RCCE_CONSTANT, "RCCE_Linear": unreal.RichCurveExtrapolation.RCCE_LINEAR, "RCCE_Cycle": unreal.RichCurveExtrapolation.RCCE_CYCLE, "RCCE_CycleWithOffset": unreal.RichCurveExtrapolation.RCCE_CYCLE_WITH_OFFSET, "RCCE_Oscillate": unreal.RichCurveExtrapolation.RCCE_OSCILLATE,
}
# ------------------------------------


def get_rich_curve_property(curve_asset):
    """
    CurveFloatアセットからRichCurveオブジェクトを、複数のプロパティ名を試して取得します。
    """
    for prop_name in RICH_CURVE_PROPERTY_NAMES:
        try:
            # get_editor_propertyでアクセスを試行
            rich_curve = curve_asset.get_editor_property(prop_name)
            # 取得したものがunreal.RichCurve型であることを確認
            if isinstance(rich_curve, unreal.RichCurve):
                print(f"✅ RichCurveプロパティ名: '{prop_name}' を特定しました。")
                return rich_curve, prop_name
        except Exception as e:
            # 失敗した場合は次のプロパティ名を試す
            print(f"⚠️ 試行 '{prop_name}' 失敗: {e}")
            continue
    return None, None


def update_single_asset_repeatedly(base_dir):
    """
    D01.jsonからD81.jsonまでを読み込み、単一のターゲットアセットに上書きを繰り返します。
    """
    print("\n--- UE5 CurveFloat アセット更新開始 (上書きモード) ---")
    print(f"🎯 上書きターゲット: {TARGET_CURVE_ASSET_PATH}")
    
    # ターゲットアセットを読み込む
    curve = unreal.EditorAssetLibrary.load_asset(TARGET_CURVE_ASSET_PATH)

    if not curve:
        print(f"🚨 致命的エラー: ターゲットアセットが見つかりません: {TARGET_CURVE_ASSET_PATH}")
        print("処理を中断しました。")
        return

    # 2. RichCurveオブジェクトを取得 (フォールバックロジックを使用)
    rich_curve, rich_curve_prop_name = get_rich_curve_property(curve)
    
    if not rich_curve:
        print(f"🚨 致命的エラー: 試行した {len(RICH_CURVE_PROPERTY_NAMES)} 種類のプロパティ名すべてでRichCurveプロパティを特定できませんでした。")
        print("💡 以前判明したとおり、この既存アセットへの直接アクセスはプロパティ保護されている可能性が高いです。処理を中断します。")
        return

    # D01からD81までループ
    update_count = 0
    
    for i in range(1, 82):
        file_name = f"D{i:02d}.json"
        json_path = os.path.join(base_dir, file_name)
        
        # 1. JSONファイルを読み込む
        try:
            with open(json_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            continue
        except json.JSONDecodeError as e:
            print(f"🚨 警告: JSONファイルの形式が不正です。スキップします: {json_path} - {e}")
            continue

        curve_data = data["floatCurve"]
        keys = curve_data["keys"]

        # 3. 既存キー削除
        keys_to_delete = [k.time for k in rich_curve.get_keys()]
        for k_time in keys_to_delete:
            rich_curve.delete_key(k_time)

        # 4. 新しいキーを追加
        for k in keys:
            new_key = rich_curve.add_key(k["time"], k["value"])

            new_key.interp_mode = INTERP_MODE_MAP.get(k["interpMode"], unreal.RichCurveInterpMode.RCIM_CUBIC)
            new_key.tangent_mode = TANGENT_MODE_MAP.get(k["tangentMode"], unreal.RichCurveTangentMode.RCTM_USER)
            new_key.tangent_weight_mode = TANGENT_WEIGHT_MODE_MAP.get(k["tangentWeightMode"], unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_NONE)

            new_key.arrive_tangent = k["arriveTangent"]
            new_key.arrive_tangent_weight = k["arriveTangentWeight"]
            new_key.leave_tangent = k["leaveTangent"]
            new_key.leave_tangent_weight = k["leaveTangentWeight"]

        # 5. その他のプロパティを更新
        rich_curve.default_value = curve_data["defaultValue"]
        rich_curve.pre_infinity_extrap = EXTRAP_MAP.get(curve_data["preInfinityExtrap"], unreal.RichCurveExtrapolation.RCCE_CONSTANT)
        rich_curve.post_infinity_extrap = EXTRAP_MAP.get(curve_data["postInfinityExtrap"], unreal.RichCurveExtrapolation.RCCE_CONSTANT)

        # 6. CurveFloat アセットに書き戻し、保存
        curve.set_editor_property(rich_curve_prop_name, rich_curve)
        unreal.EditorAssetLibrary.save_asset(TARGET_CURVE_ASSET_PATH)
        
        update_count += 1
        if i % 10 == 0 or i == 81:
            print(f"✅ 上書き: {file_name} のデータを {TARGET_CURVE_ASSET_PATH} に適用し、保存しました。")
        
    print(f"\n--- 処理完了 ---")
    print(f"合計 {update_count} 個のJSONファイルでアセットが上書きされました。最終データは D{update_count:02d}.json の内容です。")

# --- メイン実行部分 ---

if __name__ == "__main__":
    update_single_asset_repeatedly(BASE_DIR)