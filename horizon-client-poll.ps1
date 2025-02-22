Import-Module Omnissa.Hv.Helper
Import-Module Omnissa.VIMAutomation.HorizonView

# Connect to the Horizon server
$HorizonServer = "your-connection-server.domain"

# Retrieve securely stored credentials
$CredentialPath = "$env:USERPROFILE\HorizonCreds.xml"
if (Test-Path $CredentialPath) {
    $Credential = Import-Clixml -Path $CredentialPath
} else {
    Write-Host "Credential file not found. Please run 'Get-Credential | Export-Clixml' first."
    Exit
}

Connect-HVServer -Server $HorizonServer -Credential $Credential

# Generate a timestamp for the filename (YYYYMMDDHHMMSS)
$Timestamp = Get-Date -Format "yyyyMMddHHmmss"
$ExportFile = ".\horizon_client_data\HorizonClientData_$Timestamp.csv"

# Retrieve session data and extract relevant fields
Get-HVLocalSession | ForEach-Object {
    $sessionNames = $_.NamesData    # Extract NamesData properties
    $sessionData = $_.SessionData   # Extract SessionData properties

    [PSCustomObject]@{
        UserName     = $sessionNames.UserName
        MachineName  = $sessionNames.MachineOrRDSServerName
        AgentVersion = $sessionNames.AgentVersion
        ClientAddress = $sessionNames.ClientAddress
        ClientName   = $sessionNames.ClientName
        ClientVersion = $sessionNames.ClientVersion
        StartTime    = $sessionData.StartTime
    }
} | Export-Csv -Path $ExportFile -NoTypeInformation -Append

Write-Host "Session data exported successfully to $ExportFile"

# Disconnect from Horizon
Disconnect-HVServer -Confirm:$false

Write-Host "Disconnected from Horizon server."