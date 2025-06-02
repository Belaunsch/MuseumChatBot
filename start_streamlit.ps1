# PowerShell-Skript zum Starten der Streamlit App für MuseumChatBotv2
# Führt aus: streamlit run streamlit_app.py

Write-Host "🏛️ Starte Museum Guide Bot v2 - Streamlit Interface..." -ForegroundColor Cyan

# Überprüfen ob streamlit installiert ist
try {
    $streamlitVersion = streamlit --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Streamlit ist installiert: $streamlitVersion" -ForegroundColor Green
    } else {
        throw "Streamlit nicht gefunden"
    }
} catch {
    Write-Host "❌ Streamlit ist nicht installiert!" -ForegroundColor Red
    Write-Host "Installieren Sie es mit: pip install streamlit" -ForegroundColor Yellow
    exit 1
}

# Überprüfen ob die streamlit_app.py existiert
if (-not (Test-Path "streamlit_app.py")) {
    Write-Host "❌ streamlit_app.py nicht gefunden!" -ForegroundColor Red
    Write-Host "Stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden." -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Starte Streamlit Interface..." -ForegroundColor Green
Write-Host "📝 Die App wird automatisch in Ihrem Browser geöffnet" -ForegroundColor Yellow
Write-Host "🔗 URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "" 
Write-Host "💡 WICHTIG: Stellen Sie sicher, dass der Rasa Server läuft:" -ForegroundColor Yellow
Write-Host "   - Öffnen Sie ein weiteres Terminal" -ForegroundColor White
Write-Host "   - Führen Sie aus: rasa run --enable-api --cors `"*`"" -ForegroundColor White
Write-Host ""
Write-Host "⭐ Drücken Sie Ctrl+C um die App zu beenden" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray

# Streamlit App starten
streamlit run streamlit_app.py
