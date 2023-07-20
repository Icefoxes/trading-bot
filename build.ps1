$buildFolder = "hades-ui\build"
if (Test-Path $buildFolder) {
  Remove-Item $buildFolder -Force
}


$envFile = "hades-ui\.env"
if (Test-Path $envFile) {
  Remove-Item $envFile
}

$env:HOST='http://localhost:8000/api/v1'

Set-Location hades-ui

"REACT_APP_DOMAIN='$env:HOST'" > .env

npm run build