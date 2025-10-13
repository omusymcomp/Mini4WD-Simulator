import unreal, json, os

# Blueprint Class をロード（Blueprint のクラスを直接ロードする）
vehicle_class = unreal.load_blueprint_class("/Game/BluePrints/Vheicle/BP_SimpleVehicle.BP_SimpleVehicle")

# CDO (Class Default Object) を取得
vehicle_cdo = vehicle_class.get_default_object()

# Movement Component を取得
movement_component = vehicle_cdo.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)

if movement_component is None:
    unreal.log_error("ChaosWheeledVehicleMovementComponent が見つかりません")
else:
    engine = movement_component.get_editor_property("EngineSetup")
    transmission = movement_component.get_editor_property("TransmissionSetup")
    differential = movement_component.get_editor_property("DifferentialSetup")
    steering = movement_component.get_editor_property("SteeringSetup")

    # JSON にまとめる
    params = {
        "MaxTorque": engine.get_editor_property("MaxTorque"),
        "MaxRPM": engine.get_editor_property("MaxRPM"),
        "EngineIdleRPM": engine.get_editor_property("EngineIdleRPM"),
        "FinalRatio": transmission.get_editor_property("FinalRatio"),
        "FrontRearSplit": differential.get_editor_property("FrontRearSplit"),
        "SteeringAngleRatio": steering.get_editor_property("AngleRatio"),
    }

    save_path = os.path.join(unreal.Paths.project_saved_dir(), "BP_SimpleVehicle_Params.json")
    with open(save_path, "w") as f:
        json.dump(params, f, indent=4)

    unreal.log("パラメータを書き出しました: " + save_path)
