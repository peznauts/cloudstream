@ECHO OFF
SET mypath=%~dp0
cd %mypath:~0,-1%

bash -c "bash venv-install.sh"
if %ERRORLEVEL% == 0 goto :next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Installation failed.')"
goto :endofscript

:next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Installation complete.')"

:endofscript
echo "Script complete"
