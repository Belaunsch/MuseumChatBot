"""
Streamlit Interface für MuseumChatBotv2
Ein modernes Web-Interface für den Museum Guide Chatbot

Features:
- Echtzeit-Chat mit dem Rasa Bot
- Schöne UI mit Chat-Bubbles
- Sidebar mit Bot-Informationen
- Session-Management
- Beispiel-Fragen für schnellen Einstieg
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Konfiguration
RASA_API_URL = "http://localhost:5005"
BOT_NAME = "Museum Guide Bot"
BOT_VERSION = "v2.0"

def init_session_state():
    """Initialisiert den Session State für den Chat"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Begrüßungsnachricht hinzufügen
        st.session_state.messages.append({
            "sender": "bot",
            "text": "Hallo! Ich bin Ihr persönlicher Museum Guide. Ich kann Ihnen bei Fragen zu Kunstwerken, Künstlern und unserem Museum helfen. Wie kann ich Ihnen heute behilflich sein?",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"streamlit_{int(time.time())}"

def send_message_to_rasa(message: str, sender_id: str) -> List[Dict[str, Any]]:
    """Sendet eine Nachricht an den Rasa Bot und gibt die Antwort zurück"""    
    try:
        response = requests.post(
            f"{RASA_API_URL}/webhooks/rest/webhook",
            json={
                "sender": sender_id,
                "message": message
            },
            timeout=10
        )
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            error_msg = f"Entschuldigung, es gab einen Fehler bei der Verbindung zum Bot (Status: {response.status_code})."
            return [{"text": error_msg}]
    
    except requests.exceptions.ConnectionError:
        error_msg = "❌ Verbindung zum Bot fehlgeschlagen. Ist der Rasa Server gestartet?\n\nStarten Sie den Server mit: `rasa run --enable-api --cors \"*\"`"
        return [{"text": error_msg}]
    except requests.exceptions.Timeout:
        error_msg = "⏱️ Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es erneut."
        return [{"text": error_msg}]
    except Exception as e:
        error_msg = f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}"
        return [{"text": error_msg}]

def display_chat_message(message: Dict[str, Any], is_user: bool = False):
    """Zeigt eine Chat-Nachricht an"""
    if is_user:
        st.chat_message("user").write(message["text"])
    else:
        st.chat_message("assistant").write(message["text"])

def check_rasa_server():
    """Überprüft, ob der Rasa Server läuft"""
    try:
        response = requests.get(f"{RASA_API_URL}/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Hauptfunktion der Streamlit App"""
    
    # Seitenkonfiguration
    st.set_page_config(
        page_title="Museum Guide Bot v2",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS für besseres Styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin: 5px 0;
    }
    .main-header {
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .status-online {
        background-color: rgba(46, 204, 113, 0.2);
        border-left: 4px solid #2ecc71;
    }
    .status-offline {
        background-color: rgba(231, 76, 60, 0.2);
        border-left: 4px solid #e74c3c;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🏛️ Museum Guide Bot v2</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 18px;">Ihr persönlicher digitaler Museumsführer</p>', unsafe_allow_html=True)
    
    # Session State initialisieren
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Bot Information")
        
        # Server Status prüfen
        server_online = check_rasa_server()
        
        if server_online:
            st.markdown(
                '<div class="status-box status-online">✅ <strong>Bot Status:</strong> Online</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-box status-offline">❌ <strong>Bot Status:</strong> Offline</div>', 
                unsafe_allow_html=True
            )
            st.warning("⚠️ Rasa Server ist nicht erreichbar!\n\nStarten Sie den Server mit:\n```\nrasa run --enable-api --cors \"*\"\n```")
        
        st.markdown(f"**Version:** {BOT_VERSION}")
        st.markdown(f"**Session ID:** `{st.session_state.session_id}`")
        st.markdown(f"**Nachrichten:** {len(st.session_state.messages)}")
        
        st.markdown("---")
        
        # Chat zurücksetzen
        if st.button("🗑️ Chat zurücksetzen", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = f"streamlit_{int(time.time())}"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ Über den Bot")
        st.markdown("""
        Dieser Bot kann Ihnen helfen bei:
        - 🎨 **Kunstwerken** und deren Geschichte
            - z.B. "Was ist die Sternennacht?"
        - 👨‍🎨 **Künstlern** und Biografien  
            - z.B. "Was ist die Biographie von Vincent van Gogh?"

        """)
    
    # Hauptchat-Bereich
    st.markdown("### 💬 Chat")
    
    # Chat-Container
    chat_container = st.container()
    
    with chat_container:
        # Alle bisherigen Nachrichten anzeigen
        for message in st.session_state.messages:
            if message["sender"] == "user":
                st.chat_message("user").write(f"{message['text']}")
            else:
                st.chat_message("assistant").write(f"{message['text']}")
    
    # Chat Input
    if prompt := st.chat_input("Stellen Sie Ihre Frage über Kunst, Künstler oder das Museum..."):
        if not server_online:
            st.error("❌ Der Rasa Server ist nicht erreichbar. Bitte starten Sie den Server zuerst.")
            return
        
        # Benutzernachricht zur Historie hinzufügen
        st.session_state.messages.append({
            "sender": "user",
            "text": prompt,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Benutzernachricht anzeigen
        st.chat_message("user").write(prompt)
        
        # Bot-Antwort abrufen
        with st.chat_message("assistant"):
            with st.spinner("Der Bot denkt nach..."):
                bot_responses = send_message_to_rasa(prompt, st.session_state.session_id)
            
            # Bot-Antworten verarbeiten und anzeigen
            for response in bot_responses:
                response_text = response.get("text", "Entschuldigung, ich konnte keine Antwort generieren.")
                st.write(response_text)
                
                # Antwort zur Historie hinzufügen
                st.session_state.messages.append({
                    "sender": "bot",
                    "text": response_text,
                    "timestamp": datetime.now().strftime("%H:%M")
                })

if __name__ == "__main__":
    main()
