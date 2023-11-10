@echo off
set username=pxy

:: Prompt for the password
set /p password=Enter the password for the %username% account: 

:: Create a new user account
net user %username% %password% /add

:: Add the new user to the Administrators group
net localgroup Administrators %username% /add

:: Display user information
net user %username%

echo Local administrator account with username "%username%" has been created.
pause
