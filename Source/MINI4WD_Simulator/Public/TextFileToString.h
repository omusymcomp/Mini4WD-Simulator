// Fill out your copyright notice in the Description page of Project Settings.
#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "TextFileToString.generated.h"

/**
 * テキストファイルを読み込み、その内容をFStringとして取得するBlueprint関数ライブラリ
 */
UCLASS()
class AMBITIONEARLYHOURSKY_API UTextFileToString : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "File I/O")
	static void TextFileLoadToString(
		FString Filename,
		FString& FileData,
		bool& Success
	);
};