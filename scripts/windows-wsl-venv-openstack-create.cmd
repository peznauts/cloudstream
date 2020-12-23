@ECHO OFF
SET mypath=%~dp0
cd %mypath:~0,-1%

bash -c "bash ansible-exec-openstack-create.sh"
if %ERRORLEVEL% == 0 goto :next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Create failed.')"
goto :endofscript

:next
PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Create complete. Copy your stream URL from the terminal output.')"

:endofscript
echo "Script complete"
