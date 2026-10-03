[[ PAGE 1 ]]

# Runas in Powershell for Windows 10

Running some applications from menu start in Windows 10 as different user is a little tricky. You can try to click on application icon in the same time holding `Shift` button, to see additional option, but it doesn’t work on all applications. Especially not on these pinned to Menu Start.

![runas](runas.jpg)

You can `Run as different user` option in two ways.

## Enable runas in registry

To enable a registry value to show `Run as different user` in the right-click menu (in Windows 10 Start screen). Copy the following lines to Notepad, and save the file with `.reg` extension. For example: `showrunas.reg`

```powershell
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Explorer]
"ShowRunAsDifferentUserInStart"=dword:00000001
```

Now just double click on `showrunas.reg`. Logoff and login back, or restart Explorer shell for the change to take effect.

## Use runas Powershell command

Open Powershell and run command:

```powershell
runas /user:username@domain "mmc.exe dsa.msc"
```

In this example you will run Microsoft Management Console with Active Directory Users and Computers snap-in. Just change `username` and `domain` value.

## Runas script

I also wrote a small and simple script that allows you to start (as different user and custom domain) the Active Directory snap-in (dsa.msc), Active Directory Administrative Center (dsac.exe) and any other application provided as a path to executable file.

Copy below code and save as `runas.ps1` file.

```powershell
function Show-Menu
{
     param (
           [string]$Title = 'Run as different user'
     )
     cls
     Write-Host "===================== $Title ====================="

     Write-Host "1: Press '1' Active Directory User And Computers (dsa.msc)"
     Write-Host "2: Press '2' Active Directory Administrative Center (dsac.exe)"
     Write-Host "3: Press '3' Custom App (Path to app)"
     Write-Host "Q: Press 'Q' to quit."
}
do
{
     Show-Menu
     $input = Read-Host "Please make a selection"
     switch ($input)
     {
           '1' {
                cls
				$user = Read-Host -Prompt 'Enter username'
				$domain = Read-Host -Prompt 'Enter domain'
				runas /netonly /user:$user@$domain "mmc.exe dsa.msc"
           } '2' {
                cls
				$user = Read-Host -Prompt 'Enter username'
				$domain = Read-Host -Prompt 'Enter domain'
				runas /netonly /user:$user@$domain "dsac.exe"
		   } '3' {
                cls
				$user = Read-Host -Prompt 'Enter username'
				$domain = Read-Host -Prompt 'Enter domain'
				$path = Read-Host -Prompt 'Enter path'
				runas /netonly /user:$user@$domain "$path"
           }'q' {
                return
           }
     }
     pause
}
until ($input -eq 'q')
```

Run this script in PowerShell and follow instructions on screen.

![runas powershell](runaspowershell.jpg)
