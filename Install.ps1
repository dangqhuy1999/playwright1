#Copy File from NAS IT


$sourcePath = "\\192.168.12.81\data\setup\*"
$destinationPath = "D:\IT-Only\App"


if (-Not (Test-Path -Path $destinationPath)) {
    try {
        # Create a new directory at the destination path
        New-Item -ItemType Directory -Path $destinationPath -ErrorAction Stop
        Write-Host "Created directory: $destinationPath"
    } catch {
        Write-Host "Failed to create directory: $destinationPath"
        exit
    }
}


try {
    Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force -ErrorAction Stop
    Write-Host "Files copied successfully from $sourcePath to $destinationPath"
} catch {
    Write-Host "Failed to copy files from $sourcePath to $destinationPath"
}





#Install all files


$folderPath = "D:\IT-Only\App"
$exeFiles = Get-ChildItem -Path $folderPath -Filter *.exe -ErrorAction SilentlyContinue
$msiFiles = Get-ChildItem -Path $folderPath -Filter *.msi -ErrorAction SilentlyContinue
$installerFiles = @()
if ($exeFiles) { $installerFiles += $exeFiles }
if ($msiFiles) { $installerFiles += $msiFiles }
if ($installerFiles.Count -eq 0) {
    Write-Host "No .exe or .msi files found in the specified folder."
} else {
    foreach ($file in $installerFiles) {
        Write-Host "Installing $($file.Name)..."
        Start-Process -FilePath $file.FullName -ArgumentList '/silent', '/quiet' -Wait
        Write-Host "$($file.Name) installation completed."
    }
}
