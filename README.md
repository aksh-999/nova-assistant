# Nova — Personal AI Voice Assistant

Nova is a personal AI voice assistant built with Python, designed to go beyond simple chat.

The goal is to build a desktop AI assistant that can **listen, understand, remember, speak, and interact with the user's computer** through voice and natural language.

> **Nova is being built as a personal AI operating layer for the desktop.**

---

## ✨ What Nova Can Do

### 🎙️ Voice Interaction

* Speech-to-text using Faster-Whisper
* Natural voice responses using local text-to-speech
* Desktop voice interaction through a PySide6 interface
* Designed for hands-free interaction

### 🧠 AI Brain

* Gemini API integration
* Ollama support for local AI models
* Graceful handling of temporary AI-service failures
* Designed so the AI provider can evolve without rebuilding the entire assistant

### 🧩 Computer Control

Nova can currently interact with the Windows environment through Python tools.

Examples:

```text
"Open Notepad"
"Open Spotify"
"Open Discord"
"Close Notepad"
```

Nova automatically discovers installed Windows applications through Start Menu shortcuts.

### 🌐 Web Interaction

Nova can:

* Open websites
* Search Google
* Search YouTube
* Launch browser-based tasks

Example:

```text
"Search YouTube for machine learning tutorials"
"Search Google for Stanford CS229"
```

### 🧠 Memory

Nova includes a local SQLite memory system.

It can store information such as:

```text
"Remember that I'm building FounderOS."
```

and retrieve relevant saved information later.

Memory is stored locally and is intentionally excluded from Git.

### 📸 Computer Vision / Screenshots

Nova can capture screenshots of the desktop using PyAutoGUI.

This provides a foundation for future computer-use capabilities.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │  Voice / Text Input │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Nova Desktop     │
                    │      PySide6        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌─────────────────┐              ┌─────────────────┐
     │ Speech-to-Text  │              │   Text Input    │
     │ Faster-Whisper  │              │                 │
     └────────┬────────┘              └────────┬────────┘
              │                                │
              └────────────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Nova Assistant    │
                    │   Core Controller   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          ┌──────────┐   ┌──────────┐   ┌──────────┐
          │ Memory   │   │  Router  │   │ AI Brain │
          │ SQLite   │   │  Tools   │   │ Gemini / │
          │          │   │          │   │ Ollama   │
          └──────────┘   └────┬─────┘   └──────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
                  Apps     Browser   Screenshots

                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text-to-Speech    │
                    │       pyttsx3       │
                    └──────────┬──────────┘
                               │
                               ▼
                            🔊 Nova
```

---

# 📁 Project Structure

```text
nova-assistant/
│
├── app/
│   ├── core/
│   │   ├── assistant.py
│   │   ├── ai_brain.py
│   │   └── router.py
│   │
│   ├── memory/
│   │   └── memory.py
│   │
│   ├── tools/
│   │   ├── apps.py
│   │   ├── browser.py
│   │   └── screenshots.py
│   │
│   ├── ui/
│   │   └── desktop.py
│   │
│   ├── voice/
│
```
