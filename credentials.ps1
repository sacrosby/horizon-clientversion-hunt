#Store credentials in user profile on local machine -- run once

$Cred = Get-Credential
$Cred | Export-Clixml -Path "$env:USERPROFILE\HorizonCreds.xml"
