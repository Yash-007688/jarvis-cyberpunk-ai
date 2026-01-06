import React, { useRef, useEffect, useState } from 'react';
import { Mic, MicOff, Send } from 'lucide-react';

const Transcript = () => {
    const scrollRef = useRef(null);
    const [messages, setMessages] = useState([
        { id: 1, type: 'system', text: 'Initializing visual interface. Version 3.4.1 online.' },
        { id: 2, type: 'system', text: 'Voice systems online. Ready for audio input.' },
    ]);
    const [isListening, setIsListening] = useState(false);
    const [inputText, setInputText] = useState('');

    // Speech Recognition Setup
    const recognition = useRef(null);

    useEffect(() => {
        if ('webkitSpeechRecognition' in window) {
            recognition.current = new window.webkitSpeechRecognition();
            recognition.current.continuous = false;
            recognition.current.interimResults = false;

            recognition.current.onstart = () => {
                setIsListening(true);
            };

            recognition.current.onend = () => {
                setIsListening(false);
            };

            recognition.current.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                setInputText(transcript);
                handleSendMessage(transcript);
            };
        }
    }, []);

    const speak = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            // Try to find a "technological" sounding voice
            const voices = window.speechSynthesis.getVoices();
            const techVoice = voices.find(v => v.name.includes('Google US English') || v.name.includes('Microsoft David'));
            if (techVoice) utterance.voice = techVoice;

            utterance.pitch = 0.9;
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }
    };

    const handleSendMessage = async (text) => {
        if (!text.trim()) return;

        // Add User Message
        const userMsg = { id: Date.now(), type: 'user', text: text };
        setMessages(prev => [...prev, userMsg]);
        setInputText('');

        // Send to Backend API
        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: text }),
            });

            const data = await response.json();

            if (response.ok) {
                const aiText = data.reply;
                const aiMsg = {
                    id: Date.now() + 1,
                    type: 'system',
                    text: aiText,
                    action: data.action,
                    systemResult: data.system_result
                };
                setMessages(prev => [...prev, aiMsg]);

                // Speak only the main response, not file contents
                const speakText = data.action ? aiText.split('\n')[0] : aiText;
                speak(speakText);
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        } catch (error) {
            console.error("API Error:", error);
            const errorMsg = { id: Date.now() + 1, type: 'system', text: `ERROR: Could not connect to neural core. ${error.message}` };
            setMessages(prev => [...prev, errorMsg]);
            speak("System error. Connection failed.");
        }
    };

    const toggleListening = () => {
        if (isListening) {
            recognition.current.stop();
        } else {
            recognition.current.start();
        }
    };

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="h-full flex flex-col font-mono text-xs relative">
            <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar mb-2" ref={scrollRef}>
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`p-3 border-l-2 rounded-r-md ${msg.type === 'system'
                            ? 'border-cyber-cyan bg-cyber-cyan/5 text-cyber-cyan'
                            : 'border-cyber-green bg-cyber-green/5 text-cyber-green'
                            }`}
                    >
                        <div className="flex justify-between items-center mb-1 opacity-50 text-[10px] uppercase">
                            <span className="flex items-center gap-1">
                                {msg.type}
                                {msg.action && (
                                    <span className="text-cyber-green">
                                        [{msg.action.replace('_', ' ')}]
                                    </span>
                                )}
                            </span>
                            <span>{new Date().toLocaleTimeString()}</span>
                        </div>
                        <div className="leading-relaxed whitespace-pre-wrap break-words">
                            {msg.text}
                        </div>

                        {/* Show system operation results */}
                        {msg.systemResult && msg.systemResult.success && (
                            <div className="mt-2 p-2 bg-cyber-dark/50 border border-cyber-green/30 rounded text-[10px] max-h-48 overflow-y-auto">
                                {msg.action === 'read_file' && msg.systemResult.content && (
                                    <pre className="text-cyber-green/80 whitespace-pre-wrap break-words font-mono">
                                        {msg.systemResult.content}
                                    </pre>
                                )}
                                {msg.action === 'list_directory' && msg.systemResult.items && (
                                    <div className="space-y-1">
                                        {msg.systemResult.items.map((item, idx) => (
                                            <div key={idx} className="flex items-center gap-2">
                                                <span className={item.type === 'directory' ? 'text-cyber-cyan' : 'text-cyber-green'}>
                                                    {item.type === 'directory' ? '📁' : '📄'}
                                                </span>
                                                <span className="text-cyber-green/80">{item.name}</span>
                                                {item.size && (
                                                    <span className="text-cyber-cyan/50 text-[9px]">
                                                        ({(item.size / 1024).toFixed(1)} KB)
                                                    </span>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {/* Music: Current Track Info */}
                                {msg.action === 'music_current' && msg.systemResult.track_name && (
                                    <div className="flex gap-3 items-center">
                                        {msg.systemResult.album_art && (
                                            <img
                                                src={msg.systemResult.album_art}
                                                alt="Album Art"
                                                className="w-16 h-16 rounded border border-cyber-cyan/30"
                                            />
                                        )}
                                        <div className="flex-1">
                                            <div className="text-cyber-cyan font-bold">{msg.systemResult.track_name}</div>
                                            <div className="text-cyber-green/70">{msg.systemResult.artist}</div>
                                            <div className="text-cyber-cyan/50 text-[9px]">{msg.systemResult.album}</div>
                                            <div className="text-cyber-green/50 text-[9px] mt-1">
                                                {msg.systemResult.is_playing ? '▶️ Playing' : '⏸️ Paused'}
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {/* Music: Search Results */}
                                {msg.action === 'music_search' && msg.systemResult.tracks && (
                                    <div className="space-y-2">
                                        <div className="text-cyber-cyan font-bold mb-2">
                                            Found {msg.systemResult.count} tracks:
                                        </div>
                                        {msg.systemResult.tracks.map((track, idx) => (
                                            <div key={idx} className="flex items-center gap-2 p-1 hover:bg-cyber-cyan/10 rounded">
                                                <span className="text-cyber-green">🎵</span>
                                                <div className="flex-1">
                                                    <div className="text-cyber-cyan">{track.name}</div>
                                                    <div className="text-cyber-green/60 text-[9px]">{track.artist}</div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {/* Music: Now Playing (after play_song) */}
                                {msg.action === 'music_play_song' && msg.systemResult.track && (
                                    <div className="flex items-center gap-2">
                                        <span className="text-cyber-green text-xl">🎵</span>
                                        <div>
                                            <div className="text-cyber-cyan font-bold">{msg.systemResult.track.name}</div>
                                            <div className="text-cyber-green/70 text-[9px]">{msg.systemResult.track.artist}</div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ))}

                {isListening && (
                    <div className="flex items-center space-x-2 text-cyber-red animate-pulse p-2">
                        <div className="w-2 h-2 bg-cyber-red rounded-full"></div>
                        <span>LISTENING...</span>
                    </div>
                )}
            </div>

            <div className="mt-auto pt-2 border-t border-cyber-cyan/20 flex gap-2">
                <button
                    onClick={toggleListening}
                    className={`p-2 rounded border transition-all ${isListening
                        ? 'bg-cyber-red/20 border-cyber-red text-cyber-red shadow-neon-red'
                        : 'bg-cyber-dark/50 border-cyber-cyan/30 text-cyber-cyan hover:bg-cyber-cyan/20'
                        }`}
                >
                    {isListening ? <MicOff size={16} /> : <Mic size={16} />}
                </button>

                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputText)}
                    placeholder="ENTER COMMAND..."
                    className="flex-1 bg-cyber-dark/50 border border-cyber-cyan/30 rounded px-3 py-2 text-cyber-cyan placeholder-cyber-cyan/30 focus:outline-none focus:border-cyber-cyan focus:shadow-neon-cyan transition-all"
                />

                <button
                    onClick={() => handleSendMessage(inputText)}
                    className="p-2 bg-cyber-dark/50 border border-cyber-cyan/30 rounded text-cyber-cyan hover:bg-cyber-cyan/20 transition-all"
                >
                    <Send size={16} />
                </button>
            </div>
        </div>
    );
};

export default Transcript;
