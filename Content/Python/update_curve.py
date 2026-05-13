import json
import os
import sys

try:
    import unreal
except ImportError:
    print("🚨 エラー: unrealモジュールが見つかりません。このスクリプトはUnreal EngineエディタのPythonコンソールで実行してください。")
    sys.exit(1)

# --- 設定 ---

# JSONファイルが保存されているディレクトリのパス
BASE_DIR = r"C:\Users\takumi\Documents\Mini4WD-Simulator\Content\Python"

# 🎯 上書き対象となる単一のCurveFloatアセットのパスと名前
TARGET_ASSET_PATH = "/Game/BluePrints/Vheicle/HyperDash_M"
TARGET_ASSET_NAME = "HyperDash_M"
PACKAGE_PATH = os.path.dirname(TARGET_ASSET_PATH)

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


def update_single_asset_repeatedly(base_dir):
    """
    既存アセットを削除 -> 新規作成 (ファクトリ動的生成) -> D01からD81まで上書きを繰り返します。
    """
    print("\n--- UE5 CurveFloat アセット更新開始 ---")
    print(f"🎯 上書きターゲット (削除 & 再作成): {TARGET_ASSET_PATH}")
    
    # AssetToolsモジュールを取得 (アセット作成に使用)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 1. 既存アセットの削除 (プロパティ保護回避のため)
    if unreal.EditorAssetLibrary.does_asset_exist(TARGET_ASSET_PATH):
        print("🗑️ 既存アセットを削除します...")
        if unreal.EditorAssetLibrary.delete_asset(TARGET_ASSET_PATH):
            print("✅ 既存アセットの削除に成功しました。")
        else:
            print(f"🚨 致命的エラー: 既存アセットの削除に失敗しました。アセットがエディタで開かれていないか、使用中ではないか確認してください: {TARGET_ASSET_PATH}")
            return
    else:
        print("💡 既存アセットが見つかりません。新規作成のみ実行します。")


    # 2. 新しいCurveFloatアセットを同じパスに作成 (ファクトリを動的に取得)
    print("✨ 新規CurveFloatアセットを作成します...")
    
    # ファクトリクラスを動的に検索
    factory_class = unreal.find_class(None, "CurveFloatFactoryNew")
    if not factory_class:
        print("🚨 致命的エラー: CurveFloatFactoryNew クラスが見つかりません。")
        return
        
    # ファクトリインスタンスを作成
    factory_instance = unreal.new_object(factory_class)

    # アセット作成を実行
    curve = asset_tools.create_asset(
        asset_name=TARGET_ASSET_NAME,
        package_path=PACKAGE_PATH,
        asset_class=unreal.CurveFloat.static_class(),
        factory=factory_instance
    )
    
    if not curve:
        print(f"🚨 致命的エラー: アセットの新規作成に失敗しました: {TARGET_ASSET_PATH}")
        return

    # 3. RichCurveオブジェクトを取得 (新規作成直後は 'float_curve' でアクセス可能と想定)
    try:
        rich_curve = curve.get_editor_property("float_curve")
        print(f"✅ RichCurveプロパティ名: 'float_curve' を特定しました。上書き処理を開始します。")
    except Exception as e:
        print(f"🚨 致命的エラー: 新規作成したアセットのプロパティ 'float_curve' の取得に失敗しました。")
        print(f"エラー詳細: {e}")
        return
    
    # D01からD81までループ
    update_count = 0
    
    for i in range(1, 82):
        file_name = f"D{i:02d}.json"
        json_path = os.path.join(base_dir, file_name)
        
        # 4. JSONファイルを読み込む
        try:
            with open(json_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            # print(f"🚨 警告: JSONファイルが見つかりません。スキップします: {json_path}")
            continue
        except json.JSONDecodeError as e:
            print(f"🚨 警告: JSONファイルの形式が不正です。スキップします: {json_path} - {e}")
            continue

        curve_data = data["floatCurve"]
        keys = curve_data["keys"]

        # 5. 既存キー削除
        keys_to_delete = [k.time for k in rich_curve.get_keys()]
        for k_time in keys_to_delete:
            rich_curve.delete_key(k_time)

        # 6. 新しいキーを追加
        for k in keys:
            new_key = rich_curve.add_key(k["time"], k["value"])

            new_key.interp_mode = INTERP_MODE_MAP.get(k["interpMode"], unreal.RichCurveInterpMode.RCIM_CUBIC)
            new_key.tangent_mode = TANGENT_MODE_MAP.get(k["tangentMode"], unreal.RichCurveTangentMode.RCTM_USER)
            new_key.tangent_weight_mode = TANGENT_WEIGHT_MODE_MAP.get(k["tangentWeightMode"], unreal.RichCurveTangentWeightMode.RCTWM_WEIGHTED_NONE)

            new_key.arrive_tangent = k["arriveTangent"]
            new_key.arrive_tangent_weight = k["arriveTangentWeight"]
            new_key.leave_tangent = k["leaveTangent"]
            new_key.leave_tangent_weight = k["leaveTangentWeight"]

        # 7. その他のプロパティを更新
        rich_curve.default_value = curve_data["defaultValue"]
        rich_curve.pre_infinity_extrap = EXTRAP_MAP.get(curve_data["preInfinityExtrap"], unreal.RichCurveExtrapolation.RCCE_CONSTANT)
        rich_curve.post_infinity_extrap = EXTRAP_MAP.get(curve_data["postInfinityExtrap"], unreal.RichCurveExtrapolation.RCCE_CONSTANT)

        # 8. CurveFloat アセットに書き戻し、保存
        curve.set_editor_property("float_curve", rich_curve)
        unreal.EditorAssetLibrary.save_asset(TARGET_ASSET_PATH)
        
        update_count += 1
        # ログを簡略化
        if i % 10 == 0 or i == 81:
            print(f"✅ 上書き: {file_name} のデータを {TARGET_ASSET_PATH} に適用し、保存しました。")
        
    print(f"\n--- 処理完了 ---")
    print(f"合計 {update_count} 個のJSONファイルでアセットが上書きされました。最終データは D{update_count:02d}.json の内容です。")

# --- メイン実行部分 ---

if __name__ == "__main__":
    update_single_asset_repeatedly(BASE_DIR)