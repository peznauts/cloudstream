@ECHO OFF
SET mypath=%~dp0
cd %mypath:~0,-1%

bash -c "bash ansible-exec-ec2-delete.sh"
if %ERRORLEVEL% == 0 goto :next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Cleanup failed.')"
goto :endofscript

:next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Cleanup complete.')"

:endofscript
echo "Script complete"
