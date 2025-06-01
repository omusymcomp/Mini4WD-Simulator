#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "Curves/CurveFloat.h"
#include "MyPawn.generated.h"

UCLASS()
class YOURPROJECT_API AMyPawn : public APawn
{
	GENERATED_BODY()

public:
	AMyPawn();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	// 🔽 この関数を追加
	UFUNCTION(BlueprintCallable, Category = "Torque")
	void ExportTorqueCurveToCSV(const FRuntimeFloatCurve& Curve, const FString& FileName);
};
