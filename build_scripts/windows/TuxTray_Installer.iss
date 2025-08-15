; TuxTray Windows Installer Script (Inno Setup)
; =====================================================
; Creates a professional Windows installer for TuxTray
; Supports Windows 10/11, proper uninstall, registry entries

#define MyAppName "TuxTray"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Aravind Lal"
#define MyAppURL "https://github.com/mfscpayload-690/TuxTray"
#define MyAppExeName "TuxTray.exe"
#define MyAppDescription "Intelligent System Monitor with Animated Penguin"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{8C9D2F3A-4B5E-4A7C-9D8E-1F2A3B4C5D6E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
InfoBeforeFile=..\..\README.md
OutputDir=..\..\dist\installer
OutputBaseFilename=TuxTray-{#MyAppVersion}-Windows-Setup
SetupIconFile=..\..\assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
MinVersion=10.0.19041
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Start {#MyAppName} automatically when Windows starts"; GroupDescription: "Startup Options"

[Files]
Source: "..\..\dist\TuxTray\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; Tasks: desktopicon
Name: "{autostartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\assets"
Type: filesandordirs; Name: "{app}\config"
Type: files; Name: "{app}\*.log"

[Registry]
; Application registration for Windows 10/11
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey

[Code]
// Custom installer code

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  NetFrameworkInstalled: Boolean;
begin
  // Check if .NET Framework is available (for some dependencies)
  NetFrameworkInstalled := RegKeyExists(HKLM, 'SOFTWARE\Microsoft\.NETFramework\policy\v4.0') or 
                          RegKeyExists(HKLM, 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4');
  
  if not NetFrameworkInstalled then
  begin
    if MsgBox('TuxTray requires .NET Framework 4.0 or later for optimal performance. Continue installation?', 
              mbConfirmation, MB_YESNO) = IDNO then
      Result := False
    else
      Result := True;
  end
  else
    Result := True;
end;

procedure InitializeWizard();
begin
  // Custom welcome message
  WizardForm.WelcomeLabel2.Caption := 
    'This will install {#MyAppName} {#MyAppVersion} on your computer.' + #13#10#13#10 +
    '{#MyAppName} is an intelligent system monitor featuring an animated ' +
    'penguin that reacts to your system''s resource usage with 5 different ' +
    'emotional states.' + #13#10#13#10 +
    'Click Next to continue, or Cancel to exit Setup.';
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  // Validate installation directory
  if (CurPageID = wpSelectDir) then
  begin
    if Length(WizardDirValue()) > 100 then
    begin
      MsgBox('Installation path is too long. Please choose a shorter path.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create application settings directory
    CreateDir(ExpandConstant('{app}\config'));
    
    // Set up file associations or additional configuration if needed
    // (Currently not needed for TuxTray)
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // Skip component selection page (we don't have components)
  if PageID = wpSelectComponents then
    Result := True
  else
    Result := False;
end;

// Uninstaller code
function InitializeUninstall(): Boolean;
var
  UninstallString: String;
begin
  // Ask user if they want to remove configuration files
  if MsgBox('Do you want to remove TuxTray configuration files and saved settings?', 
            mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
  begin
    // Remove user configuration files
    DelTree(ExpandConstant('{userappdata}\TuxTray'), True, True, True);
  end;
  
  Result := True;
end;
