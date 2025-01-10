// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "RamaColorPicker.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
struct FLinearColor;
#ifdef VICTORYBPLIBRARY_RamaColorPicker_generated_h
#error "RamaColorPicker.generated.h already included, missing '#pragma once' in RamaColorPicker.h"
#endif
#define VICTORYBPLIBRARY_RamaColorPicker_generated_h

#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_14_DELEGATE \
VICTORYBPLIBRARY_API void FOnJoyColorChangedEvent_DelegateWrapper(const FMulticastScriptDelegate& OnJoyColorChangedEvent, FLinearColor const& NewColor);


#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_RPC_WRAPPERS \
	DECLARE_FUNCTION(execSetJoyColor);


#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_INCLASS \
private: \
	static void StaticRegisterNativesURamaColorPicker(); \
	friend struct Z_Construct_UClass_URamaColorPicker_Statics; \
public: \
	DECLARE_CLASS(URamaColorPicker, UWidget, COMPILED_IN_FLAGS(0), CASTCLASS_None, TEXT("/Script/VictoryBPLibrary"), NO_API) \
	DECLARE_SERIALIZER(URamaColorPicker)


#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_STANDARD_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API URamaColorPicker(const FObjectInitializer& ObjectInitializer = FObjectInitializer::Get()); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(URamaColorPicker) \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, URamaColorPicker); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(URamaColorPicker); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	URamaColorPicker(URamaColorPicker&&); \
	URamaColorPicker(const URamaColorPicker&); \
public: \
	NO_API virtual ~URamaColorPicker();


#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_19_PROLOG
#define FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_GENERATED_BODY_LEGACY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_RPC_WRAPPERS \
	FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_INCLASS \
	FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h_22_STANDARD_CONSTRUCTORS \
public: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> VICTORYBPLIBRARY_API UClass* StaticClass<class URamaColorPicker>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_UnrealProjects_ProjectCPP55_PluginStaging_Output55_HostProject_Plugins_VictoryBPLibrary_Source_VictoryBPLibrary_Public_RamaColorPicker_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
