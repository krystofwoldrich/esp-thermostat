
$deps = @(
  "https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/MQTT/umqttsimple.py";
)

foreach ($dep in $deps) {
  curl -O -J -L $dep
}

Write-Host "Dependencies downloaded" -ForegroundColor Green
