# Build QwenPaw portable Windows package using PyInstaller.
# Run on Windows from repo root: pwsh -File scripts/pack/build_portable_win.ps1
#
# Prerequisites:
#   - Python 3.10 with qwenpaw[full] installed
#   - Node.js / npm (for building console frontend)
#   - PyInstaller: pip install pyinstaller
#   - (Optional) NSIS: for creating Setup.exe installer

$ErrorActionPreference = "Stop"
$RepoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $RepoRoot
Write-Host "[build_portable] REPO_ROOT=$RepoRoot"

# ---- Step 1: Build console frontend ----
Write-Host "`n== Step 1: Building console frontend =="
$ConsoleDir = Join-Path $RepoRoot "console"
$ConsoleDest = Join-Path $RepoRoot "src\qwenpaw\console"

Push-Location $ConsoleDir
try {
    npm ci
    if ($LASTEXITCODE -ne 0) { throw "npm ci failed" }
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "npm run build failed" }
} finally {
    Pop-Location
}

# Copy frontend to package dir
if (Test-Path $ConsoleDest) {
    Remove-Item -Path (Join-Path $ConsoleDest "*") -Recurse -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Force -Path $ConsoleDest | Out-Null
}
Copy-Item -Path (Join-Path $ConsoleDir "dist\*") -Destination $ConsoleDest -Recurse -Force
Write-Host "[build_portable] Console frontend copied."

# ---- Step 2: Build wheel ----
Write-Host "`n== Step 2: Building wheel =="
python -m pip install --quiet build
$DistDir = Join-Path $RepoRoot "dist"
if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
}
python -m build --outdir dist .
if ($LASTEXITCODE -ne 0) { throw "python -m build failed" }
Write-Host "[build_portable] Wheel built."

# ---- Step 3: Create temp venv and install ----
Write-Host "`n== Step 3: Creating temp venv and installing qwenpaw =="
$VenvDir = Join-Path $RepoRoot ".venv-portable"
if (Test-Path $VenvDir) { Remove-Item -Recurse -Force $VenvDir }

python -m venv $VenvDir
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip = Join-Path $VenvDir "Scripts\pip.exe"

& $VenvPython -m pip install --upgrade pip
$WheelFile = (Get-ChildItem -Path (Join-Path $DistDir "qwenpaw-*.whl") | Select-Object -First 1).FullName
& $VenvPython -m pip install "$WheelFile[full]"
if ($LASTEXITCODE -ne 0) { throw "pip install qwenpaw failed" }

# Verify
& $VenvPython -c "import qwenpaw; print(f'qwenpaw OK')"
& $VenvPython -c "import certifi; print(f'certifi OK')"

# ---- Step 4: Install PyInstaller ----
Write-Host "`n== Step 4: Installing PyInstaller =="
& $VenvPython -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { throw "pip install pyinstaller failed" }

# ---- Step 5: Run PyInstaller ----
Write-Host "`n== Step 5: Running PyInstaller =="
& $VenvPython -m PyInstaller scripts\pack\qwenpaw.spec --noconfirm
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

# Verify output
$ExePath = Join-Path $RepoRoot "dist\QwenPaw\QwenPaw.exe"
if (Test-Path $ExePath) {
    $size = (Get-Item $ExePath).Length / 1MB
    Write-Host "[build_portable] QwenPaw.exe built ($([math]::Round($size, 1)) MB)"
} else {
    throw "QwenPaw.exe not found!"
}

$DebugExePath = Join-Path $RepoRoot "dist\QwenPaw-Debug\QwenPaw-Debug.exe"
if (Test-Path $DebugExePath) {
    Write-Host "[build_portable] QwenPaw-Debug.exe also built."
}

# ---- Step 6: (Optional) Build NSIS installer ----
$NsisAvailable = $false
try {
    $null = Get-Command makensis -ErrorAction Stop
    $NsisAvailable = $true
} catch {
    Write-Host "[build_portable] NSIS not found, skipping installer build."
}

if ($NsisAvailable) {
    Write-Host "`n== Step 6: Building NSIS installer =="
    $VerFile = Join-Path $RepoRoot "src\qwenpaw\__version__.py"
    $Version = ""
    foreach ($line in Get-Content $VerFile) {
        if ($line -match '__version__\s*=\s*"([^"]+)"') {
            $Version = $Matches[1]
            break
        }
    }
    if (-not $Version) { $Version = "0.0.0" }

    $NsiContent = @"
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "scripts\pack\assets\icon.ico"
!define MUI_UNICON "scripts\pack\assets\icon.ico"

Name "QwenPaw Desktop"
OutFile "dist\QwenPaw-Setup-$Version.exe"
InstallDir `$LOCALAPPDATA\QwenPaw
InstallDirRegKey HKCU "Software\QwenPaw" "InstallPath"
RequestExecutionLevel user

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "QwenPaw Desktop" SEC01
  SetOutPath "`$INSTDIR"
  File /r "dist\QwenPaw\*.*"
  WriteRegStr HKCU "Software\QwenPaw" "InstallPath" "`$INSTDIR"
  WriteUninstaller "`$INSTDIR\Uninstall.exe"
  CreateShortcut "`$SMPROGRAMS\QwenPaw Desktop.lnk" "`$INSTDIR\QwenPaw.exe" "" "`$INSTDIR\QwenPaw.exe" 0
  CreateShortcut "`$DESKTOP\QwenPaw Desktop.lnk" "`$INSTDIR\QwenPaw.exe" "" "`$INSTDIR\QwenPaw.exe" 0
  CreateShortcut "`$SMPROGRAMS\QwenPaw Desktop (Debug).lnk" "`$INSTDIR\QwenPaw-Debug\QwenPaw-Debug.exe" "" "`$INSTDIR\QwenPaw-Debug\QwenPaw-Debug.exe" 0
SectionEnd

Section "Uninstall"
  Delete "`$SMPROGRAMS\QwenPaw Desktop.lnk"
  Delete "`$SMPROGRAMS\QwenPaw Desktop (Debug).lnk"
  Delete "`$DESKTOP\QwenPaw Desktop.lnk"
  RMDir /r "`$INSTDIR"
  DeleteRegKey HKCU "Software\QwenPaw"
SectionEnd
"@
    $NsiContent | Set-Content -Path (Join-Path $DistDir "portable.nsi") -Encoding ASCII
    makensis (Join-Path $DistDir "portable.nsi")
    if ($LASTEXITCODE -ne 0) { throw "makensis failed" }

    $SetupExe = Join-Path $DistDir "QwenPaw-Setup-$Version.exe"
    if (Test-Path $SetupExe) {
        $size = (Get-Item $SetupExe).Length / 1MB
        Write-Host "[build_portable] NSIS installer: $SetupExe ($([math]::Round($size, 1)) MB)"
    }
}

# ---- Cleanup ----
Write-Host "`n== Cleanup =="
if (Test-Path $VenvDir) {
    Remove-Item -Recurse -Force $VenvDir
    Write-Host "[build_portable] Removed temp venv."
}

Write-Host "`n== Build complete! =="
Write-Host "  Portable:  dist\QwenPaw\QwenPaw.exe"
Write-Host "  Debug:     dist\QwenPaw-Debug\QwenPaw-Debug.exe"
if ($NsisAvailable) {
    Write-Host "  Installer: dist\QwenPaw-Setup-*.exe"
}
