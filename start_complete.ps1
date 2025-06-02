# PowerShell-Skript zum vollständigen Starten des MuseumChatBotv2 Systems
# Startet sowohl Rasa Server als auch Streamlit Interface

param(
    [switch]$OnlyStreamlit,
    [switch]$OnlyRasa,
    [switch]$OnlyActions,
    [switch]$Help
)

if ($Help) {
    Write-Host "Museum Guide Bot v2 - Vollstaendiger Start" -ForegroundColor Cyan
    Write-Host ""    Write-Host "Parameter:" -ForegroundColor Yellow
    Write-Host "  -OnlyStreamlit  : Nur Streamlit Interface starten" -ForegroundColor White
    Write-Host "  -OnlyRasa       : Nur Rasa Server starten" -ForegroundColor White
    Write-Host "  -OnlyActions    : Nur Actions Server starten" -ForegroundColor White
    Write-Host "  -Help           : Diese Hilfe anzeigen" -ForegroundColor White
    Write-Host ""
    Write-Host "Beispiele:" -ForegroundColor Yellow
    Write-Host "  .\start_complete.ps1                 # Startet alles" -ForegroundColor White
    Write-Host "  .\start_complete.ps1 -OnlyStreamlit  # Nur Streamlit" -ForegroundColor White
    Write-Host "  .\start_complete.ps1 -OnlyRasa       # Nur Rasa" -ForegroundColor White
    exit 0
}

Write-Host "Museum Guide Bot v2 - System Start" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Funktion: Actions Server starten
function Start-ActionsServer {
    Write-Host "Starte Actions Server..." -ForegroundColor Green
    
    # Überprüfen ob actions Ordner existiert
    if (-not (Test-Path "actions")) {
        Write-Host "Actions Ordner nicht gefunden!" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Starte Actions Server auf Port 5055..." -ForegroundColor Yellow
    Start-Process -FilePath "rasa" -ArgumentList "run", "actions", "--debug" -PassThru
    
    # Warten bis Server bereit ist
    Write-Host "Warte auf Actions Server..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    return $true
}

# Funktion: Rasa Server starten
function Start-RasaServer {
    Write-Host "Starte Rasa Server..." -ForegroundColor Green
    
    # Überprüfen ob rasa installiert ist
    try {
        $rasaVersion = rasa --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Rasa ist installiert: $rasaVersion" -ForegroundColor Green
        } else {
            throw "Rasa nicht gefunden"
        }
    } catch {
        Write-Host "Rasa ist nicht installiert!" -ForegroundColor Red
        Write-Host "Installieren Sie es mit: pip install rasa" -ForegroundColor Yellow
        return $false
    }
    
    # Überprüfen ob Modell vorhanden ist
    if (-not (Test-Path "models")) {
        Write-Host "Kein Modell gefunden! Trainieren Sie zuerst ein Modell mit: rasa train" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Starte Rasa API Server auf Port 5005..." -ForegroundColor Yellow
    Start-Process -FilePath "rasa" -ArgumentList "run", "--enable-api", "--cors", "*", "--debug" -PassThru
    
    # Warten bis Server bereit ist
    Write-Host "Warte auf Rasa Server..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    return $true
}

# Funktion: Streamlit Interface starten  
function Start-StreamlitApp {
    Write-Host "Starte Streamlit Interface..." -ForegroundColor Green
    
    # Überprüfen ob streamlit installiert ist
    try {
        $streamlitVersion = streamlit --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Streamlit ist installiert: $streamlitVersion" -ForegroundColor Green
        } else {
            throw "Streamlit nicht gefunden"
        }
    } catch {
        Write-Host "Streamlit ist nicht installiert!" -ForegroundColor Red
        Write-Host "Installieren Sie es mit: pip install streamlit" -ForegroundColor Yellow
        return $false
    }
    
    # Überprüfen ob streamlit_app.py existiert
    if (-not (Test-Path "streamlit_app.py")) {
        Write-Host "streamlit_app.py nicht gefunden!" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Starte Streamlit auf Port 8501..." -ForegroundColor Yellow
    Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
    
    Start-Process -FilePath "streamlit" -ArgumentList "run", "streamlit_app.py" -PassThru
    return $true
}

# Hauptlogik
if ($OnlyRasa) {
    if (Start-RasaServer) {
        Write-Host "Rasa Server gestartet!" -ForegroundColor Green
        Write-Host "API verfügbar unter: http://localhost:5005" -ForegroundColor Cyan
    } else {
        Write-Host "Fehler beim Starten des Rasa Servers" -ForegroundColor Red
        exit 1
    }
} elseif ($OnlyStreamlit) {
    if (Start-StreamlitApp) {
        Write-Host "Streamlit Interface gestartet!" -ForegroundColor Green
        Write-Host "Stellen Sie sicher, dass der Rasa Server läuft (Port 5005)" -ForegroundColor Yellow
    } else {
        Write-Host "Fehler beim Starten der Streamlit App" -ForegroundColor Red
        exit 1
    }
} elseif ($OnlyActions) {
    if (Start-ActionsServer) {
        Write-Host "Actions Server gestartet!" -ForegroundColor Green
        Write-Host "API verfügbar unter: http://localhost:5055" -ForegroundColor Cyan
    } else {
        Write-Host "Fehler beim Starten des Actions Servers" -ForegroundColor Red
        exit 1
    }
} else {
    # Alle Services starten
    Write-Host "Starte vollständiges System..." -ForegroundColor Green
    
    # Zuerst Actions Server
    if (Start-ActionsServer) {
        Write-Host "Actions Server läuft" -ForegroundColor Green
        
        # Dann Rasa Server
        Start-Sleep -Seconds 2
        if (Start-RasaServer) {
            Write-Host "Rasa Server läuft" -ForegroundColor Green
            
            # Dann Streamlit
            Start-Sleep -Seconds 3
            if (Start-StreamlitApp) {
                Write-Host "Streamlit Interface läuft" -ForegroundColor Green
                Write-Host ""
                Write-Host "System vollständig gestartet!" -ForegroundColor Green
                Write-Host "Actions Server: http://localhost:5055" -ForegroundColor Cyan
                Write-Host "Rasa API: http://localhost:5005" -ForegroundColor Cyan
                Write-Host "Streamlit: http://localhost:8501" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Drücken Sie Ctrl+C um alle Prozesse zu beenden" -ForegroundColor Magenta
                
                # Warten auf Benutzer-Eingabe
                try {
                    Write-Host "Drücken Sie eine beliebige Taste zum Beenden..." -ForegroundColor Yellow
                    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                } catch {
                    # Fallback für Systeme ohne RawUI
                    Read-Host "Drücken Sie Enter zum Beenden"
                }
            } else {
                Write-Host "Fehler beim Starten der Streamlit App" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "Fehler beim Starten des Rasa Servers" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Fehler beim Starten des Actions Servers" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Auf Wiedersehen!" -ForegroundColor Green
