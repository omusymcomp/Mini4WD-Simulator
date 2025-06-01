void AMyPawn::ExportTorqueCurveToCSV(const FRuntimeFloatCurve& Curve, const FString& FileName)
{
	FString OutputString = "RPM,Torque\n";
	const FRichCurve* RichCurve = Curve.GetRichCurveConst();

	if (!RichCurve)
	{
		UE_LOG(LogTemp, Warning, TEXT("RichCurve is invalid."));
		return;
	}

	for (auto It = RichCurve->GetKeyIterator(); It; ++It)
	{
		const FRichCurveKey& Key = *It;
		OutputString += FString::Printf(TEXT("%.2f,%.2f\n"), Key.Time, Key.Value);
	}

	FString FullPath = FPaths::ProjectDir() + FileName;

	if (FFileHelper::SaveStringToFile(OutputString, *FullPath))
	{
		UE_LOG(LogTemp, Log, TEXT("Torque curve exported to: %s"), *FullPath);
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to export torque curve to: %s"), *FullPath);
	}
}
