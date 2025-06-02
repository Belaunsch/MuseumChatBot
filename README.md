# Museum Guide Chatbot v2 🏛️🎨

Ein interaktiver Museums-Guide-Chatbot, entwickelt mit Rasa und einem Streamlit-Webinterface. Der Bot beantwortet Fragen zu Kunstwerken, Künstlern, Kunstrichtungen und Museumsinformationen und nutzt dafür unter anderem die Wikipedia API für dynamische Inhalte.

## 🌟 Hauptmerkmale

*   **Interaktives Chat-Interface:** Benutzerfreundliche Weboberfläche erstellt mit Streamlit.
*   **Dynamische Wissensabfrage:**
    *   Informationen zu **Kunstrichtungen** (z.B. Impressionismus, Barock) über die Wikipedia API.
    *   **Künstler-Biografien** (Wikipedia API).
    *   *(Optional erweiterbar)* Informationen zu spezifischen **Kunstwerken** (z.B. über MET Museum API).
    *   *(Optional erweiterbar)* **Museums-Informationen** wie Öffnungszeiten (z.B. über Google Places API).
*   **Konversationsgestützte KI:**
    *   Verständnis natürlicher Sprache (NLU) für flexible Anfragen.
    *   Dialogmanagement zur Führung kontextbezogener Unterhaltungen.
*   **Modulare Action-Struktur:** Klare Trennung der Logik für verschiedene Informationsbeschaffungen.

## 🚀 Installation und Setup

### Voraussetzungen
*   Python 3.8 oder höher
*   pip (Python Package Manager)
*   Git

### Schritt 1: Repository klonen
```bash
git clone <repository-url>
cd MuseumChatBotv2
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)
```bash
python -m venv venv
# Auf Windows (PowerShell):
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# venv\Scripts\activate
# Auf macOS/Linux:
# source venv/bin/activate
```
Bitte aktivieren Sie die virtuelle Umgebung in jedem neuen Terminal, in dem Sie mit dem Projekt arbeiten.

### Schritt 3: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Schritt 4: API-Keys konfigurieren (falls spezifische APIs genutzt werden)
Falls APIs genutzt werden, die einen Key benötigen (z.B. Google Places API für Museums-Informationen, falls aktiviert):
1.  Erstellen Sie eine Datei `.env` im Hauptverzeichnis (`MuseumChatBotv2/.env`).
2.  Fügen Sie Ihre API-Keys im folgenden Format hinzu:
    ```
    GOOGLE_PLACES_API_KEY=IHR_GOOGLE_PLACES_API_KEY_HIER
    # Weitere API-Keys hier
    ```
    Das Projekt ist so konfiguriert, dass `python-dotenv` diese Variablen automatisch lädt.

### Schritt 5: Rasa-Modell trainieren
Dieser Schritt ist notwendig, um das NLU-Modell und die Dialogmanagement-Modelle zu erstellen.
```bash
rasa train
```

## 🏃‍♂️ Bot starten

Der Chatbot besteht aus zwei Hauptkomponenten, die parallel laufen müssen: dem **Rasa Server** (für die Chatbot-Logik) und dem **Streamlit Interface** (für die Benutzeroberfläche).

### Schritt 1: Rasa Action Server starten
Der Action Server führt Ihren benutzerdefinierten Python-Code aus (z.B. API-Aufrufe).
Öffnen Sie ein Terminal, aktivieren Sie die virtuelle Umgebung und führen Sie aus:
```bash
rasa run actions
```

### Schritt 2: Rasa Server starten
Der Rasa Server stellt die API bereit, mit der das Streamlit-Interface kommuniziert.
Öffnen Sie ein **zweites** Terminal, aktivieren Sie die virtuelle Umgebung und führen Sie aus:
```bash
rasa run --enable-api --cors "*" --debug
```
*   `--enable-api`: Macht den Server über HTTP erreichbar.
*   `--cors "*"`: Erlaubt Anfragen von jeder Domain (wichtig für das lokale Streamlit-Interface).
*   `--debug`: Zeigt detaillierte Log-Ausgaben, hilfreich für die Entwicklung.

Der Rasa Server ist dann unter `http://localhost:5005` erreichbar.

### Schritt 3: Streamlit Interface starten
Das Streamlit Interface bietet die grafische Benutzeroberfläche für den Chat.
Öffnen Sie ein **drittes** Terminal, aktivieren Sie die virtuelle Umgebung und führen Sie das bereitgestellte PowerShell-Skript aus (oder passen Sie es für Ihre Shell an):
```bash
# Für Windows PowerShell im MuseumChatBotv2 Verzeichnis:
./start_streamlit.ps1
```
Alternativ können Sie Streamlit auch direkt starten:
```bash
streamlit run streamlit_app.py
```
Das Streamlit-Interface wird normalerweise automatisch in Ihrem Browser unter `http://localhost:8501` geöffnet.

## 🛠️ Wichtige Dateien und Projektstruktur

```
MuseumChatBotv2/
├── actions/                       # Verzeichnis für benutzerdefinierte Rasa-Aktionen
│   ├── __init__.py                # Macht das actions-Verzeichnis zu einem Python-Package
│   ├── actions.py                 # Haupt-Dispatch-Datei für Actions (importiert spezifische Actions)
│   ├── comprehensive_actions.py   # Enthält komplexere Actions wie ActionFetchArtInfo
│   ├── artwork_actions.py         # (Beispiel) Actions speziell für Kunstwerke
│   ├── artist_actions.py          # (Beispiel) Actions speziell für Künstler
│   ├── museum_actions.py          # (Beispiel) Actions speziell für Museumsinfos
│   └── utils/                     # Hilfsfunktionen für die Actions
│       ├── __init__.py            # Macht das utils-Verzeichnis zu einem Python-Package
│       ├── api_clients.py         # (Beispiel) Clients für externe APIs (z.B. Wikipedia, MET)
│       ├── text_processing.py     # (Beispiel) Funktionen zur Textbereinigung, Zusammenfassung
│       └── logger_config.py       # (Beispiel) Konfiguration für das Logging-System
│
├── data/                          # Trainingsdaten für Rasa
│   ├── nlu.yml                    # NLU-Trainingsbeispiele (Intents, Entities, Beispiele)
│   ├── rules.yml                  # Regeln für einfache, oft zustandslose Dialogabläufe
│   └── stories.yml                # Beispielhafte Dialogpfade für das Training des Modells
│
├── models/                        # Hier speichert Rasa die trainierten Modelle (tar.gz-Dateien)
│
├── tests/                         # Testdateien für Ihren Chatbot (optional, aber empfohlen)
│   └── ...                        # z.B. test_stories.yml, test_nlu.yml, tests_actions.py
│
├── .env                           # Lokale Umgebungsvariablen (API-Keys etc.) - NICHT IN GIT!
├── .env_example                   # Beispieldatei für Umgebungsvariablen (API-Keys etc.)
├── .gitignore                     # Definiert Dateien/Ordner, die von Git ignoriert werden sollen
├── config.yml                     # Konfiguration für die NLU-Pipeline und Dialogue Policies
├── credentials.yml                # Konfiguration für externe Kanäle, hier meist Standard
├── domain.yml                     # Definiert das "Universum" des Bots: Intents, Entities, Slots, Responses, Actions
├── endpoints.yml                  # Konfiguration der Endpunkte, insbesondere des Action Servers
├── requirements.txt               # Liste der Python-Abhängigkeiten für das Projekt
├── streamlit_app.py               # Python-Skript für das Streamlit Web-Interface
├── start_streamlit.ps1            # PowerShell-Skript zum einfachen Starten des Streamlit-Interfaces
├── README.md                      # Diese Datei: Projektübersicht und Anleitung
└── (weitere Skripte/Dateien)
```

### Detaillierte Dateibeschreibungen:

*   **`config.yml`**: Definiert die NLU-Pipeline (wie Text verarbeitet und Intents/Entities extrahiert werden, z.B. Tokenizer, Featurizer, Classifier) und die Dialogue Policies (Algorithmen, die entscheiden, welche Aktion der Bot als Nächstes ausführt, z.B. TEDPolicy, RulePolicy).
*   **`domain.yml`**: Das Herzstück des Bots. Hier werden alle Intents (Benutzerabsichten, z.B. `ask_art_movement`), Entities (Informationen, die aus Nutzereingaben extrahiert werden, z.B. `art_movement`), Slots (Variablen, die Informationen während eines Gesprächs speichern), Responses (vordefinierte Antworttexte des Bots, `utter_...`) und Custom Actions (programmierbare Aktionen, `action_...`) deklariert.
*   **`credentials.yml`**: Dient zur Konfiguration von Verbindungen zu externen Chat-Plattformen (z.B. Slack, Facebook Messenger, Twilio). Für eine reine Web-Anwendung mit Streamlit, die direkt mit dem Rasa HTTP-Server kommuniziert, ist hier oft keine spezielle Konfiguration über die Standardeinstellungen hinaus nötig.
*   **`endpoints.yml`**: Konfiguriert externe Endpunkte. Am wichtigsten ist hier der `action_endpoint`, der dem Rasa-Server mitteilt, unter welcher URL der Action Server erreichbar ist (standardmäßig `http://localhost:5055/webhook`). Kann auch für Datenbanken oder NLU-Model-Server genutzt werden.
*   **`requirements.txt`**: Listet alle Python-Pakete und deren Versionen auf, die für das Projekt benötigt werden (z.B. `rasa`, `streamlit`, `wikipedia`, `python-dotenv`). Wird mit `pip install -r requirements.txt` installiert.
*   **`streamlit_app.py`**: Enthält den Python-Code zur Erstellung und Ausführung des Streamlit Web-Interfaces. Diese Datei ist verantwortlich für die grafische Darstellung des Chats, das Senden von Benutzereingaben an den Rasa-Server (via HTTP-Request) und die Anzeige der vom Rasa-Server zurückgegebenen Bot-Antworten.
*   **`start_streamlit.ps1`**: Ein Hilfsskript für Windows PowerShell, das die Streamlit-App startet. Es prüft typischerweise, ob man sich im richtigen Verzeichnis befindet und gibt die URL zur App aus. Für andere Betriebssysteme können ähnliche Shell-Skripte erstellt werden.
*   **`.env`**: (Optional, aber empfohlen für API-Keys) Eine Datei zum Speichern von Umgebungsvariablen lokal. Diese Datei sollte **niemals** in Versionskontrollsysteme (wie Git) eingecheckt werden. Enthält sensible Daten wie API-Schlüssel.
*   **`.env_example`**: Eine Vorlagedatei, die zeigt, welche Umgebungsvariablen benötigt werden. Sie kann kopiert, in `.env` umbenannt und mit den tatsächlichen Werten befüllt werden.
*   **`.gitignore`**: Eine Textdatei, die festlegt, welche Dateien und Verzeichnisse von Git bei Commits ignoriert werden sollen (z.B. `venv/`, `models/`, `__pycache__/`, `.env`).
*   **`actions/` Verzeichnis**: Enthält den Python-Code für Custom Actions, die über einfache Textantworten hinausgehende Logik ausführen.
    *   **`actions/__init__.py`**: Eine leere Datei, die Python signalisiert, dass das `actions`-Verzeichnis als Package behandelt werden soll. Ermöglicht Importe von Modulen innerhalb dieses Verzeichnisses.
    *   **`actions/actions.py`**: Dient oft als Hauptdatei für Actions, die die in `domain.yml` deklarierten Actions als Klassen implementiert oder spezifischere Actions aus anderen Dateien im `actions`-Ordner importiert und für Rasa verfügbar macht. Könnte auch ein Dispatcher sein, der Actions aus Submodulen lädt.
    *   **`actions/comprehensive_actions.py`**: Enthält die Implementierung für komplexere Actions. Ein Beispiel ist `ActionFetchArtInfo`, welche die Logik zur Abfrage der Wikipedia-API, zur Verarbeitung der Ergebnisse und zur Formulierung der Antwort für Fragen zu Kunstrichtungen enthält.
    *   **`actions/utils/` Unterverzeichnis**: Sammelt Hilfsmodule und -funktionen, die von mehreren Actions gemeinsam genutzt werden können, um Code-Duplizierung zu vermeiden und die Lesbarkeit und Wartbarkeit der Actions zu verbessern.
        *   **`actions/utils/__init__.py`**: Macht das `utils`-Verzeichnis zu einem Python-Subpackage.
        *   **`actions/utils/api_clients.py`**: (Beispiel) Könnte Klassen oder Funktionen enthalten, die die spezifische Logik für die Kommunikation mit externen APIs (z.B. Wikipedia, Metropolitan Museum of Art API, Google Places API) kapseln. Dies beinhaltet das Senden von Anfragen, das Verarbeiten von Antworten und Fehlerbehandlung.
        *   **`actions/utils/text_processing.py`**: (Beispiel) Könnte Funktionen für die Aufbereitung von Texten enthalten, z.B. das Zusammenfassen von längeren Texten (wie `summarize_wikipedia_content`), das Bereinigen von HTML-Tags, oder andere NLP-bezogene Hilfsaufgaben, die in Actions benötigt werden.
        *   **`actions/utils/logger_config.py`**: (Beispiel) Könnte eine Funktion `setup_logger()` enthalten, die eine standardisierte Logger-Instanz für die Actions konfiguriert und zurückgibt, um einheitliches Logging im Projekt sicherzustellen.
*   **`data/` Verzeichnis**: Enthält alle Trainingsdaten, die Rasa benötigt, um das NLU-Modell und das Dialogmanagement-Modell zu trainieren.
    *   **`data/nlu.yml`**: Enthält die Trainingsbeispiele für das Natural Language Understanding. Hier definieren Sie Intents (z.B. `greet`, `ask_art_movement`), versehen sie mit zahlreichen Beispiel-Äußerungen von Nutzern und annotieren gegebenenfalls Entities (z.B. `[Impressionismus](art_movement)`).
    *   **`data/rules.yml`**: Definiert einfache, oft zustandslose Konversationsmuster. Regeln sind nützlich für Situationen, in denen der Bot immer gleich reagieren soll, unabhängig vom vorherigen Gesprächsverlauf (z.B. Beantwortung von `chitchat` oder Auslösen einer Aktion bei einem bestimmten Intent).
    *   **`data/stories.yml`**: Beschreibt komplexere, beispielhafte Dialogverläufe. Jede Story ist ein repräsentativer Pfad, den eine Konversation nehmen kann, und listet abwechselnd Nutzer-Intents (ggf. mit Entities) und Bot-Aktionen/Antworten auf. Sie sind entscheidend für das Training des Machine-Learning-basierten Dialogmanagements (TEDPolicy).
*   **`models/` Verzeichnis**: In diesem Verzeichnis speichert Rasa standardmäßig die trainierten Modelle. Jedes Training erzeugt eine `.tar.gz`-Datei, die das NLU- und Core-Modell enthält.
*   **`tests/` Verzeichnis**: (Optional, aber sehr empfohlen) Enthält Testfälle, um die Qualität und Korrektheit des Chatbots sicherzustellen. Dies kann NLU-Tests (`test_nlu.yml`), Conversation-Tests (`test_stories.yml`) und Tests für Custom Actions (Python Unit-Tests) umfassen.

## 🧪 Tests ausführen (Beispiele)

### NLU Tests
```bash
rasa test nlu --nlu data/nlu.yml # (oder spezifische Test-NLU-Datei)
```

### Core (Dialog) Tests
```bash
rasa test core --stories data/stories.yml # (oder spezifische Test-Story-Datei)
```

### Alle Tests
```bash
rasa test
```

## 🔧 Konfiguration der Custom Actions

Die Custom Actions in `actions/comprehensive_actions.py` (und anderen `*_actions.py` Dateien) sind für die dynamische Informationsbeschaffung zuständig.
*   **`ActionFetchArtInfo`**: Nutzt die `wikipedia` Python-Bibliothek, um Informationen zu Kunstrichtungen, Künstlern etc. abzurufen und aufzubereiten.
*   Stellen Sie sicher, dass alle in den Actions verwendeten Bibliotheken in `requirements.txt` enthalten sind.

## 🌐 Verwendete Haupttechnologien & Bibliotheken

*   **Rasa**: Open-Source-Framework für Conversational AI.
    *   **Rasa NLU**: Für das Verstehen von Nutzereingaben.
    *   **Rasa Core**: Für das Dialogmanagement.
*   **Streamlit**: Python-Bibliothek zur Erstellung von interaktiven Web-Applikationen.
*   **Wikipedia API**: Genutzt über die `wikipedia` Python-Bibliothek für den Zugriff auf Artikelinhalte.
*   **Python-Dotenv**: Zum Laden von Umgebungsvariablen aus `.env`-Dateien (z.B. für API-Keys).

## 🚀 Zukünftige Erweiterungsideen

*   Integration weiterer APIs für spezifischere Kunstwerk- oder Museumsdaten.
*   Ausbau der Mehrsprachigkeit.
*   Implementierung von Nutzer-Feedback-Mechanismen.
*   Personalisierte Tourenvorschläge basierend auf Nutzerinteressen.
*   Erweiterte multimodale Fähigkeiten (Bilderkennung, Sprachsteuerung).

## 🤝 Mitwirken

Wenn Sie zum Projekt beitragen möchten:
1.  Forken Sie das Repository.
2.  Erstellen Sie einen neuen Branch für Ihre Änderungen (`git checkout -b feature/AmazingFeature`).
3.  Machen Sie Ihre Änderungen und committen Sie diese (`git commit -m 'Add some AmazingFeature'`).
4.  Pushen Sie zum Branch (`git push origin feature/AmazingFeature`).
5.  Öffnen Sie einen Pull Request.

---

Bei Fragen oder Problemen, öffnen Sie bitte ein Issue im Repository.