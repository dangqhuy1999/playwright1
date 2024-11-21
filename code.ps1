
# Set variables
$sharedFolder = "\\truenas"
$username = "huy.dang.10295"  # You can also prompt for the username if needed
$driveLetter = "D:"

# Prompt the user for the password
$password = Read-Host -Prompt "Enter your password" -AsSecureString

# Create a credential object
$credential = New-Object System.Management.Automation.PSCredential($username, $password)

# Disconnect existing connections
if (Test-Path $driveLetter) {
    Remove-PSDrive -Name $driveLetter.Substring(0,1) -Force
}

# Connect to the shared folder
New-PSDrive -Name $driveLetter.Substring(0,1) -PSProvider FileSystem -Root $sharedFolder -Credential $credential

# Check if the connection was successful
if (Test-Path $driveLetter) {
    Write-Host "Successfully connected to $sharedFolder as $username."
} else {
    Write-Host "Failed to connect to $sharedFolder."
}

# Pause the script to see the output (optional)
Read-Host -Prompt "Press Enter to exit"