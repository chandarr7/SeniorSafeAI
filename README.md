# SeniorSafeAI
Repository for SeniorSafe AI project with Chat UI - Your trusted cybersecurity assistant for scam and fraud protection.

## About SeniorSafe AI

SeniorSafe AI is an empathetic, AI-powered chatbot designed to help seniors and vulnerable individuals who have been victims of cybercrime and online scams. It provides clear, step-by-step guidance and support for various types of cyber threats.

## Features

- **🎙️ Voice Assistant (Speech Input/Output)** - Complete hands-free interaction for accessibility (NEW!)
  - Speech recognition for voice input (speak instead of type)
  - Text-to-speech for voice output (hear responses read aloud)
  - Auto-read mode for fully hands-free operation
  - Large, senior-friendly voice controls
  - Adjustable speed, volume, and voice selection
  - Emergency keyword detection in speech
  - Works in Chrome, Edge, Safari
- **🚨 Emergency Escalation System** - Automatically detects urgent situations and provides immediate action guidance
  - Real-time detection of active scams
  - Immediate "STOP" instructions for payments in progress
  - Device compromise alerts with disconnect instructions
  - Bank fraud detection with instant bank contact guidance
  - Threat response protocols
- **8 Quick-Start Conversation Options** - Including dedicated "🚨 URGENT Help" button for emergencies
- **Local Resources Lookup** - Automatic ZIP code-based lookup for local police, state consumer protection, and federal agencies (all 50 states + DC)
- **Senior-Friendly Interface** - Large fonts, high contrast, easy-to-read design
- **Step-by-Step Guidance** - Clear instructions in simple language
- **Multiple Scam Type Support** - Identity theft, financial fraud, tech support scams, phishing, and more
- **Empathetic AI Assistant** - Patient, supportive, and reassuring responses
- **Accessible Design** - WCAG 2.1 compliant for better accessibility

## Models and Frameworks Used

- **Mistral** - Large Language Model for natural language understanding
- **LangChain** - Framework for LLM application development
- **Chainlit** - Frontend UI framework for chat interfaces
- **Python 3.8+** - Core programming language

## System Requirements

You must have Python 3.8 or later installed. 

How to Install and Run SeniorSafe AI
1. Fork this repository: 

```
git clone https://github.com/<username>/SeniorSafe_LD.git
cd SeniorSafe_LD
```


2. Create a virtualenv and activate the virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

4. Install all packages
```
pip install -r requirements.txt
```

6. Run in your terminal to start SeniorSafe AI
```
chainlit run seniorsafe_chat_ui_v1.py
```

## UI Improvements

The interface has been enhanced with senior-friendly features:

### Conversation Starters
- 8 pre-configured quick-start options for common scenarios
- Visual icons for easy identification
- One-click access to guided conversations
- NEW: "🚨 URGENT Help" starter with pulsing alert for emergency situations
- NEW: "Find Local Help" starter for ZIP code-based resource lookup

### Accessibility Features
- **Larger Text**: 18px base font size for better readability
- **High Contrast**: Optimized color schemes for both light and dark modes
- **Clear Navigation**: Intuitive interface with prominent buttons
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Enhanced User Experience
- Welcoming introduction screen with helpful information
- Empathetic and supportive AI responses
- Step-by-step instructions in simple language
- Clean, uncluttered interface design

### Local Resources Lookup (NEW)
- **Automatic ZIP Code Detection** - System detects ZIP codes in your messages
- **Comprehensive Database** - Covers all 50 US states plus DC
- **Multiple Resource Types**:
  - State Consumer Protection Offices
  - Federal Agencies (FTC, FBI IC3, IdentityTheft.gov, IRS, SSA, USPS)
  - Local Law Enforcement Guidance
- **Smart Prompting** - Asks for ZIP code when you need local help
- **Easy to Use** - Just provide your ZIP code and get instant local resources

**Example Usage:**
```
You: "Where can I report this scam?"
AI: "Please provide your ZIP code..."
You: "10001"
AI: [Provides NY state resources, federal agencies, and local guidance]
```

### Emergency Escalation System (NEW) 🚨
- **Automatic Urgency Detection** - System analyzes messages for emergency keywords
- **Real-Time Intervention** - Interrupts active scams with immediate guidance
- **Four Urgency Levels**:
  - CRITICAL: Active scams (seconds matter)
  - HIGH: Recent incidents (hours matter)
  - MEDIUM: Concerns (days matter)
  - LOW: General inquiries
- **Specific Emergency Scenarios**:
  - Active bank fraud with withdrawal in progress
  - Device compromised with remote access
  - Currently on phone with scammer
  - About to make fraudulent payment
  - Receiving threats or blackmail
- **Visual Alerts**: High-contrast red alerts with pulsing animation
- **Immediate Action Steps**: Clear, numbered instructions prioritized by urgency

**Example Emergency Detection:**
```
You: "Someone is controlling my computer right now!"
AI: 🚨 URGENT: Device Compromised - Immediate Action Required
    1. DISCONNECT FROM INTERNET IMMEDIATELY
    2. SHUT DOWN your computer
    [... detailed emergency response ...]
```

### Voice Assistant (NEW) 🎙️
- **Hands-Free Operation** - Complete voice-controlled interaction
- **Speech Recognition** - Speak your messages instead of typing
- **Text-to-Speech** - Hear responses read aloud automatically
- **Large Voice Controls**:
  - 🎤 **Speak Button** - Click and speak your message
  - 🔊 **Read Aloud Button** - Hear last response
  - ⏹️ **Stop Button** - Stop listening or reading
  - ⚙️ **Settings** - Customize voice preferences
- **Customizable Settings**:
  - Auto-read mode (hands-free)
  - Adjustable reading speed (0.5x - 1.5x)
  - Volume control (0% - 100%)
  - Voice selection (choose from available voices)
- **Emergency Detection**: Recognizes urgent keywords in speech
- **Keyboard Shortcuts**: Ctrl+Shift+V (speak), Ctrl+Shift+R (read)
- **Privacy-First**: All processing happens locally in your browser

**Example Voice Interaction:**
```
You: [Clicks 🎤 Speak button]
System: "Listening... Speak now"
You: "I need help with a phone scam my ZIP code is 90210"
System: [Transcribes → Detects emergency + ZIP → Provides resources]
AI: [Response is automatically read aloud if auto-read is on]
```

**Browser Compatibility**:
- ✅ Chrome (Recommended)
- ✅ Microsoft Edge
- ✅ Safari (Mac/iOS)
- ⚠️ Firefox (Limited)

For detailed information about UI improvements, see [UI_IMPROVEMENTS.md](UI_IMPROVEMENTS.md)

For complete local resources documentation, see [LOCAL_RESOURCES_GUIDE.md](LOCAL_RESOURCES_GUIDE.md)

For voice assistant complete guide, see [VOICE_ASSISTANT_GUIDE.md](VOICE_ASSISTANT_GUIDE.md)

For emergency escalation system details, see [EMERGENCY_ESCALATION_GUIDE.md](EMERGENCY_ESCALATION_GUIDE.md)

## Available Versions

- **seniorsafe_chat_ui_v1.py** - Enhanced version with conversation starters (recommended)
- **seniorsafe_chat_ui_general.py** - Version with RAG (Retrieval Augmented Generation)
- **seniorsafe_chat_ui_v3_logic.py** - Version with detailed scam-specific logic

## Documentation

- [UI Improvements Guide](UI_IMPROVEMENTS.md) - Detailed documentation of all UI enhancements
- [Voice Assistant Guide](VOICE_ASSISTANT_GUIDE.md) - Complete speech input/output system documentation
- [Local Resources Guide](LOCAL_RESOURCES_GUIDE.md) - Complete guide to ZIP code-based resource lookup
- [Emergency Escalation Guide](EMERGENCY_ESCALATION_GUIDE.md) - Emergency detection and response system documentation
- [Human Evaluation](Human%20evaluation/) - Guidelines for evaluating AI responses

## Support

If you need help or have questions:
1. Use the conversation starters on the main interface
2. Type your question in plain language OR click 🎤 to speak
3. Enable voice auto-read for hands-free operation
4. Review the welcome message for guidance

---

**SeniorSafe AI** - Because everyone deserves safe and secure online experiences.
