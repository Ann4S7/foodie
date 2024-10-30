$currentDir = Get-Location
$sourcePath = Join-Path -Path $currentDir -ChildPath "src"
$Env:PYTHONPATH="$sourcePath"