/**
 * Voice Input/Output System for SeniorSafe AI
 * Provides speech recognition (voice input) and text-to-speech (voice output)
 * Optimized for seniors with large buttons, clear feedback, and simple controls
 */

class VoiceAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isReading = false;
        this.autoRead = localStorage.getItem('voiceAutoRead') === 'true';
        this.voiceSpeed = parseFloat(localStorage.getItem('voiceSpeed') || '0.9');
        this.voicePitch = parseFloat(localStorage.getItem('voicePitch') || '1.0');
        this.voiceVolume = parseFloat(localStorage.getItem('voiceVolume') || '1.0');
        this.selectedVoice = localStorage.getItem('selectedVoice') || null;
        this.continuousMode = false;

        this.init();
    }

    init() {
        // Initialize Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            this.recognition.maxAlternatives = 1;

            this.setupRecognitionHandlers();
        } else {
            console.warn('Speech recognition not supported in this browser');
        }

        // Wait for voices to load
        if (this.synthesis) {
            this.synthesis.addEventListener('voiceschanged', () => {
                this.loadVoices();
            });
            this.loadVoices();
        }

        // Create voice controls UI
        this.createVoiceControls();

        // Listen for new messages to auto-read
        this.observeNewMessages();
    }

    setupRecognitionHandlers() {
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceButton('listening');
            this.showListeningIndicator();
            console.log('Voice recognition started');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update the interim results display
            this.updateInterimResults(interimTranscript);

            if (finalTranscript) {
                this.handleVoiceInput(finalTranscript);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateVoiceButton('idle');
            this.hideListeningIndicator();

            if (event.error === 'no-speech') {
                this.showNotification('No speech detected. Please try again.', 'warning');
            } else if (event.error === 'not-allowed') {
                this.showNotification('Microphone access denied. Please enable microphone permissions.', 'error');
            } else {
                this.showNotification('Error: ' + event.error, 'error');
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateVoiceButton('idle');
            this.hideListeningIndicator();
            console.log('Voice recognition ended');
        };
    }

    loadVoices() {
        const voices = this.synthesis.getVoices();

        // Prefer English voices, prioritize natural-sounding ones
        const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));

        // Try to find a good default voice
        if (!this.selectedVoice && englishVoices.length > 0) {
            // Prefer voices with "natural" or "enhanced" in the name
            const preferredVoice = englishVoices.find(v =>
                v.name.toLowerCase().includes('natural') ||
                v.name.toLowerCase().includes('enhanced') ||
                v.name.toLowerCase().includes('premium')
            ) || englishVoices[0];

            this.selectedVoice = preferredVoice.name;
        }

        // Update voice selector if it exists
        this.updateVoiceSelector(englishVoices);
    }

    updateVoiceSelector(voices) {
        const selector = document.getElementById('voice-selector');
        if (selector && voices.length > 0) {
            selector.innerHTML = voices.map(voice =>
                `<option value="${voice.name}" ${voice.name === this.selectedVoice ? 'selected' : ''}>
                    ${voice.name} (${voice.lang})
                </option>`
            ).join('');
        }
    }

    startListening() {
        if (!this.recognition) {
            this.showNotification('Speech recognition is not supported in your browser. Please try Chrome or Edge.', 'error');
            return;
        }

        if (this.isListening) {
            this.stopListening();
            return;
        }

        // Stop any ongoing speech
        if (this.isReading) {
            this.stopReading();
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start recognition:', error);
            this.showNotification('Could not start voice recognition. Please try again.', 'error');
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    handleVoiceInput(transcript) {
        console.log('Voice input received:', transcript);

        // Check for emergency keywords
        const emergencyKeywords = ['emergency', 'urgent', 'help me now', 'scam happening', 'need help immediately'];
        const isEmergency = emergencyKeywords.some(keyword =>
            transcript.toLowerCase().includes(keyword)
        );

        if (isEmergency) {
            // Visual alert for emergency
            this.showNotification('🚨 EMERGENCY DETECTED - Processing immediately', 'emergency');
        }

        // Insert the transcript into the input field
        const inputField = document.querySelector('textarea[placeholder*="Type"], textarea, input[type="text"]');
        if (inputField) {
            inputField.value = transcript;
            inputField.focus();

            // Trigger input event to update any watchers
            const event = new Event('input', { bubbles: true });
            inputField.dispatchEvent(event);

            // Auto-submit if it's a voice command
            if (this.continuousMode) {
                this.submitMessage();
            } else {
                // Show submit hint
                this.showNotification('Message ready. Click Send or say "Send message" to submit.', 'info');
            }
        }

        this.hideListeningIndicator();
    }

    submitMessage() {
        // Try to find and click the submit button
        const submitButton = document.querySelector('button[type="submit"], button[aria-label*="send" i]');
        if (submitButton) {
            submitButton.click();
        }
    }

    speakText(text, priority = 'normal') {
        if (!this.synthesis) {
            console.warn('Text-to-speech not supported');
            return;
        }

        // Clean the text for better speech
        const cleanText = this.cleanTextForSpeech(text);

        // Cancel current speech if priority is high
        if (priority === 'high' || priority === 'emergency') {
            this.synthesis.cancel();
        }

        const utterance = new SpeechSynthesisUtterance(cleanText);

        // Set voice parameters
        utterance.rate = this.voiceSpeed;
        utterance.pitch = this.voicePitch;
        utterance.volume = this.voiceVolume;

        // Select voice
        const voices = this.synthesis.getVoices();
        const selectedVoiceObj = voices.find(v => v.name === this.selectedVoice);
        if (selectedVoiceObj) {
            utterance.voice = selectedVoiceObj;
        }

        utterance.onstart = () => {
            this.isReading = true;
            this.updateReadButton('reading');
        };

        utterance.onend = () => {
            this.isReading = false;
            this.updateReadButton('idle');
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.isReading = false;
            this.updateReadButton('idle');
        };

        this.synthesis.speak(utterance);
    }

    cleanTextForSpeech(text) {
        return text
            // Remove markdown formatting
            .replace(/#{1,6}\s/g, '')
            .replace(/\*\*/g, '')
            .replace(/\*/g, '')
            .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')
            .replace(/`([^`]+)`/g, '$1')
            // Remove special characters that don't read well
            .replace(/---+/g, ', ')
            .replace(/===/g, ', ')
            // Convert bullet points
            .replace(/^\s*[-*]\s+/gm, 'Item: ')
            .replace(/^\s*\d+\.\s+/gm, 'Step $&: ')
            // Remove URLs
            .replace(/https?:\/\/[^\s]+/g, '')
            // Clean up extra whitespace
            .replace(/\n\n+/g, '. ')
            .replace(/\n/g, '. ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    stopReading() {
        if (this.synthesis) {
            this.synthesis.cancel();
            this.isReading = false;
            this.updateReadButton('idle');
        }
    }

    readLastMessage() {
        // Find the last assistant message
        const messages = document.querySelectorAll('.message-content');
        if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            const text = lastMessage.textContent || lastMessage.innerText;
            this.speakText(text, 'high');
        } else {
            this.showNotification('No messages to read', 'info');
        }
    }

    observeNewMessages() {
        // Watch for new messages and auto-read if enabled
        const observer = new MutationObserver((mutations) => {
            if (!this.autoRead) return;

            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList) {
                        // Check if this is a new message
                        if (node.classList.contains('message') ||
                            node.querySelector('.message-content')) {

                            // Wait a bit for the message to fully render
                            setTimeout(() => {
                                const content = node.querySelector('.message-content') || node;
                                const text = content.textContent || content.innerText;

                                // Only read assistant messages, not user messages
                                if (!node.classList.contains('user-message')) {
                                    this.speakText(text);
                                }
                            }, 500);
                        }
                    }
                });
            });
        });

        // Start observing the messages container
        const messagesContainer = document.querySelector('.messages, #messages, [class*="message-container"]');
        if (messagesContainer) {
            observer.observe(messagesContainer, {
                childList: true,
                subtree: true
            });
        }
    }

    createVoiceControls() {
        // Check if controls already exist
        if (document.getElementById('voice-controls-container')) {
            return;
        }

        const controlsHTML = `
            <div id="voice-controls-container" class="voice-controls">
                <div class="voice-controls-header">
                    <h3>🎙️ Voice Assistant</h3>
                    <button id="voice-settings-toggle" class="icon-button" title="Voice Settings">
                        ⚙️
                    </button>
                </div>

                <div class="voice-main-controls">
                    <button id="voice-input-btn" class="voice-btn voice-input-btn" title="Click to speak">
                        <span class="voice-icon">🎤</span>
                        <span class="voice-label">Speak</span>
                    </button>

                    <button id="voice-read-btn" class="voice-btn voice-read-btn" title="Read last message">
                        <span class="voice-icon">🔊</span>
                        <span class="voice-label">Read Aloud</span>
                    </button>

                    <button id="voice-stop-btn" class="voice-btn voice-stop-btn" title="Stop reading">
                        <span class="voice-icon">⏹️</span>
                        <span class="voice-label">Stop</span>
                    </button>
                </div>

                <div id="listening-indicator" class="listening-indicator" style="display: none;">
                    <div class="listening-animation"></div>
                    <p>Listening... Speak now</p>
                    <p class="interim-results"></p>
                </div>

                <div id="voice-settings-panel" class="voice-settings-panel" style="display: none;">
                    <h4>Voice Settings</h4>

                    <label class="voice-setting">
                        <input type="checkbox" id="auto-read-toggle" ${this.autoRead ? 'checked' : ''}>
                        <span>Automatically read responses</span>
                    </label>

                    <label class="voice-setting">
                        <span>Reading Speed</span>
                        <input type="range" id="voice-speed-slider" min="0.5" max="1.5" step="0.1" value="${this.voiceSpeed}">
                        <span class="range-value">${this.voiceSpeed}x</span>
                    </label>

                    <label class="voice-setting">
                        <span>Volume</span>
                        <input type="range" id="voice-volume-slider" min="0" max="1" step="0.1" value="${this.voiceVolume}">
                        <span class="range-value">${Math.round(this.voiceVolume * 100)}%</span>
                    </label>

                    <label class="voice-setting">
                        <span>Voice</span>
                        <select id="voice-selector" class="voice-selector"></select>
                    </label>

                    <button id="test-voice-btn" class="test-voice-btn">Test Voice</button>
                </div>

                <div id="voice-notification" class="voice-notification" style="display: none;"></div>
            </div>
        `;

        // Insert controls into the page
        document.body.insertAdjacentHTML('beforeend', controlsHTML);

        // Attach event listeners
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Voice input button
        document.getElementById('voice-input-btn')?.addEventListener('click', () => {
            this.startListening();
        });

        // Read aloud button
        document.getElementById('voice-read-btn')?.addEventListener('click', () => {
            this.readLastMessage();
        });

        // Stop button
        document.getElementById('voice-stop-btn')?.addEventListener('click', () => {
            this.stopReading();
            this.stopListening();
        });

        // Settings toggle
        document.getElementById('voice-settings-toggle')?.addEventListener('click', () => {
            const panel = document.getElementById('voice-settings-panel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        });

        // Auto-read toggle
        document.getElementById('auto-read-toggle')?.addEventListener('change', (e) => {
            this.autoRead = e.target.checked;
            localStorage.setItem('voiceAutoRead', this.autoRead);
        });

        // Speed slider
        document.getElementById('voice-speed-slider')?.addEventListener('input', (e) => {
            this.voiceSpeed = parseFloat(e.target.value);
            localStorage.setItem('voiceSpeed', this.voiceSpeed);
            e.target.nextElementSibling.textContent = `${this.voiceSpeed}x`;
        });

        // Volume slider
        document.getElementById('voice-volume-slider')?.addEventListener('input', (e) => {
            this.voiceVolume = parseFloat(e.target.value);
            localStorage.setItem('voiceVolume', this.voiceVolume);
            e.target.nextElementSibling.textContent = `${Math.round(this.voiceVolume * 100)}%`;
        });

        // Voice selector
        document.getElementById('voice-selector')?.addEventListener('change', (e) => {
            this.selectedVoice = e.target.value;
            localStorage.setItem('selectedVoice', this.selectedVoice);
        });

        // Test voice button
        document.getElementById('test-voice-btn')?.addEventListener('click', () => {
            this.speakText('Hello! This is a test of the voice assistant. I am here to help you stay safe from online scams.', 'high');
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Shift + V = Start voice input
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'V') {
                e.preventDefault();
                this.startListening();
            }
            // Ctrl/Cmd + Shift + R = Read last message
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'R') {
                e.preventDefault();
                this.readLastMessage();
            }
            // Escape = Stop reading/listening
            if (e.key === 'Escape') {
                this.stopReading();
                this.stopListening();
            }
        });
    }

    updateVoiceButton(state) {
        const btn = document.getElementById('voice-input-btn');
        if (!btn) return;

        btn.classList.remove('listening', 'processing');

        if (state === 'listening') {
            btn.classList.add('listening');
            btn.querySelector('.voice-label').textContent = 'Listening...';
        } else if (state === 'processing') {
            btn.classList.add('processing');
            btn.querySelector('.voice-label').textContent = 'Processing...';
        } else {
            btn.querySelector('.voice-label').textContent = 'Speak';
        }
    }

    updateReadButton(state) {
        const btn = document.getElementById('voice-read-btn');
        if (!btn) return;

        btn.classList.remove('reading');

        if (state === 'reading') {
            btn.classList.add('reading');
            btn.querySelector('.voice-label').textContent = 'Reading...';
        } else {
            btn.querySelector('.voice-label').textContent = 'Read Aloud';
        }
    }

    showListeningIndicator() {
        const indicator = document.getElementById('listening-indicator');
        if (indicator) {
            indicator.style.display = 'block';
        }
    }

    hideListeningIndicator() {
        const indicator = document.getElementById('listening-indicator');
        if (indicator) {
            indicator.style.display = 'none';
            const interimResults = indicator.querySelector('.interim-results');
            if (interimResults) {
                interimResults.textContent = '';
            }
        }
    }

    updateInterimResults(text) {
        const interimResults = document.querySelector('.interim-results');
        if (interimResults) {
            interimResults.textContent = text;
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.getElementById('voice-notification');
        if (!notification) return;

        notification.textContent = message;
        notification.className = 'voice-notification ' + type;
        notification.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
}

// Initialize voice assistant when page loads
let voiceAssistant;

function initVoiceAssistant() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            voiceAssistant = new VoiceAssistant();
        });
    } else {
        voiceAssistant = new VoiceAssistant();
    }
}

// Start initialization
initVoiceAssistant();

// Make voice assistant available globally for debugging
window.voiceAssistant = voiceAssistant;

console.log('🎙️ Voice Assistant loaded successfully');
