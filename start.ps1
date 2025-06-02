# Start-Skript für den Museum Guide Chatbot
# Dieses PowerShell-Skript startet alle erforderlichen Services

param(
    [switch]$Shell,    # Startet Rasa Shell für interaktive Tests
    [switch]$API,      # Startet Rasa API Server  
    [switch]$Train,    # Trainiert das Modell vor dem Start
    [switch]$Test      # Führt Tests aus
)

Write-Host "🏛️ Museum Guide Chatbot Starter 🤖" -ForegroundColor Cyan
Write-Host "=====================================`n" -ForegroundColor Cyan

# Prüfen ob Python verfügbar ist
try {
    $pythonVersion = python --version
    Write-Host "✅ Python gefunden: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python nicht gefunden. Bitte installieren Sie Python 3.8+." -ForegroundColor Red
    exit 1
}

# Prüfen ob Rasa installiert ist
try {
    $rasaVersion = rasa --version
    Write-Host "✅ Rasa gefunden: $rasaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Rasa nicht gefunden. Führen Sie 'pip install -r requirements.txt' aus." -ForegroundColor Red
    exit 1
}

# Prüfen ob .env Datei existiert
if (Test-Path ".env") {
    Write-Host "✅ .env Datei gefunden" -ForegroundColor Green
    # Laden der Umgebungsvariablen aus .env
    Get-Content .env | Where-Object { $_ -notmatch '^#' -and $_ -match '=' } | ForEach-Object {
        $key, $value = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($key, $value, [EnvironmentVariableTarget]::Process)
    }
} else {
    Write-Host "⚠️  .env Datei nicht gefunden. Kopieren Sie .env.template zu .env und konfigurieren Sie Ihre API-Keys." -ForegroundColor Yellow
}

# Modell trainieren falls gewünscht
if ($Train) {
    Write-Host "`n🎯 Trainiere Rasa Modell..." -ForegroundColor Blue
    rasa train
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Training fehlgeschlagen!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Training erfolgreich!" -ForegroundColor Green
}

# Tests ausführen falls gewünscht
if ($Test) {
    Write-Host "`n🧪 Führe Tests aus..." -ForegroundColor Blue
    rasa test
    Write-Host "✅ Tests abgeschlossen!" -ForegroundColor Green
    return
}

# Prüfen ob Modell existiert
if (-not (Test-Path "models")) {
    Write-Host "`n⚠️  Kein trainiertes Modell gefunden. Starte Training..." -ForegroundColor Yellow
    rasa train
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Training fehlgeschlagen!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🚀 Starte Museum Guide Chatbot..." -ForegroundColor Blue

if ($Shell) {
    # Interaktive Shell starten
    Write-Host "📱 Startet Rasa Shell für interaktive Tests..." -ForegroundColor Green
    Write-Host "💡 Tipp: Öffnen Sie ein zweites Terminal und führen Sie 'rasa run actions' aus.`n" -ForegroundColor Yellow
    
    Start-Sleep 2
    rasa shell
    
} elseif ($API) {
    # API Server starten
    Write-Host "🌐 Startet Rasa API Server..." -ForegroundColor Green
    Write-Host "💡 Tipp: Öffnen Sie ein zweites Terminal und führen Sie 'rasa run actions' aus." -ForegroundColor Yellow
    Write-Host "🔗 API verfügbar unter: http://localhost:5005`n" -ForegroundColor Cyan
    
    Start-Sleep 2
    rasa run --enable-api --cors "*"
    
} else {
    # Standard: Beide Services in separaten Fenstern starten
    Write-Host "🔧 Startet Action Server..." -ForegroundColor Green
    
    # Action Server in neuem PowerShell-Fenster
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '🔧 Action Server - Museum Guide Chatbot' -ForegroundColor Cyan; rasa run actions"
    
    Write-Host "📱 Warte 5 Sekunden und starte dann Rasa Shell..." -ForegroundColor Green
    Start-Sleep 5
    
    # Rasa Shell im aktuellen Fenster
    Write-Host "🤖 Rasa Shell gestartet! Schreiben Sie 'Hallo' um zu beginnen." -ForegroundColor Cyan
    Write-Host "💬 Beispiele:" -ForegroundColor Yellow
    Write-Host "   - 'Erzähl mir etwas über The Starry Night'" -ForegroundColor Gray
    Write-Host "   - 'Wer war Vincent van Gogh?'" -ForegroundColor Gray
    Write-Host "   - 'Wann öffnet das Louvre heute?'" -ForegroundColor Gray
    Write-Host "   - '/stop' zum Beenden`n" -ForegroundColor Gray
    
    rasa shell
}

Write-Host "`n👋 Museum Guide Chatbot beendet. Auf Wiedersehen!" -ForegroundColor Cyan
