; QwenPaw Desktop NSIS installer — PyInstaller portable version.
;
; This script packages the PyInstaller output (dist/QwenPaw/) into
; a single Setup.exe installer. It is designed to be invoked by the
; GitHub Actions workflow or build_portable_win.ps1.
;
; Usage:
;   makensis /DQWENPAW_VERSION=1.2.3 scripts\pack\portable.nsi

!include "MUI2.nsh"
!define MUI_ABORTWARNING

!ifndef QWENPAW_VERSION
  !define QWENPAW_VERSION "0.0.0"
!endif

; Icon paths — adjust if running from a different working directory
!define MUI_ICON "scripts\pack\assets\icon.ico"
!define MUI_UNICON "scripts\pack\assets\icon.ico"

Name "QwenPaw Desktop"
OutFile "dist\QwenPaw-Setup-${QWENPAW_VERSION}.exe"
InstallDir "$LOCALAPPDATA\QwenPaw"
InstallDirRegKey HKCU "Software\QwenPaw" "InstallPath"
RequestExecutionLevel user

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "QwenPaw Desktop" SEC01
  SetOutPath "$INSTDIR"
  File /r "dist\QwenPaw\*.*"
  WriteRegStr HKCU "Software\QwenPaw" "InstallPath" "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortcut "$SMPROGRAMS\QwenPaw Desktop.lnk" "$INSTDIR\QwenPaw.exe" "" "$INSTDIR\QwenPaw.exe" 0
  CreateShortcut "$DESKTOP\QwenPaw Desktop.lnk" "$INSTDIR\QwenPaw.exe" "" "$INSTDIR\QwenPaw.exe" 0
  CreateShortcut "$SMPROGRAMS\QwenPaw Desktop (Debug).lnk" "$INSTDIR\QwenPaw-Debug\QwenPaw-Debug.exe" "" "$INSTDIR\QwenPaw-Debug\QwenPaw-Debug.exe" 0
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\QwenPaw Desktop.lnk"
  Delete "$SMPROGRAMS\QwenPaw Desktop (Debug).lnk"
  Delete "$DESKTOP\QwenPaw Desktop.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\QwenPaw"
SectionEnd
