[Setup]
AppName=Luigi's SSH Manager
AppVersion=2.1.0
DefaultDirName={autopf}\LuigiSSHManager
DefaultGroupName=Luigi's SSH Manager
OutputDir=dist
OutputBaseFilename=LuigiSSHManager-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
ChangesEnvironment=yes

[Tasks]
Name: "envPath"; Description: "Ajouter au PATH Windows (Lancer avec 'luigi-ssh-manager' depuis n'importe où)"

[Files]
Source: "luigi-ssh-manager.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Luigi's SSH Manager"; Filename: "{app}\luigi-ssh-manager.exe"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: envPath; Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
