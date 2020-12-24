@ECHO OFF
SET mypath=%~dp0
cd %mypath:~0,-1%

for /f %%i in ('bash -c "pwd"') do set OUTPUT=%%i

IF NOT EXIST %APPDATA%\obs-studio\basic\profiles GOTO NOWINDIR
cd %APPDATA%\obs-studio\basic\profiles
:NOWINDIR

bash -c "bash %OUTPUT%/ansible-exec-ec2-create.sh"

if %ERRORLEVEL% == 0 goto :next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Create failed.')"
goto :endofscript

:next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Create complete. Copy your stream URL from the terminal output.')"

:endofscript
echo "Script complete"
