// Fill out your copyright notice in the Description page of Project Settings.

#include "TextFileToString.h"
// ファイル操作に必要なヘッダーを追加
#include "HAL/PlatformFileManager.h"
#include "Misc/FileHelper.h"

void UTextFileToString::TextFileLoadToString(FString Filename, FString& FileData, bool& Success)
{
	// 最初に失敗として初期化し、成功した場合のみtrueにする
	Success = false;
	FileData = TEXT(""); // データをクリアしておく

	// ファイルが存在するかをチェック
	if (!FPlatformFileManager::Get().GetPlatformFile().FileExists(*Filename))
	{
		// ファイルが存在しない場合はメッセージを出力（任意）
		UE_LOG(LogTemp, Warning, TEXT("File not found at path: %s"), *Filename);
		return;
	}

	// FFileHelper::LoadFileToString は、成功した場合に true を返します
	if (FFileHelper::LoadFileToString(FileData, *Filename))
	{
		Success = true;
	}
	else
	{
		// 読み込みに失敗した場合のメッセージを出力（任意）
		UE_LOG(LogTemp, Error, TEXT("Failed to load file content from: %s"), *Filename);
	}
}