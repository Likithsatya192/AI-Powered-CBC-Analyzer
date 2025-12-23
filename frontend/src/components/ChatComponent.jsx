import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Loader2, MessageSquare } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ChatComponent({ collectionName, sessionId }) {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I have analyzed the report. Ask me anything about it.' }
    ]);
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || !collectionName) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await axios.post(`${API_BASE}/chat`, {
                question: userMessage,
                collection_name: collectionName,
                session_id: sessionId
            });

            setMessages(prev => [...prev, { role: 'assistant', content: response.data.answer }]);
        } catch (error) {
            console.error("Chat Error:", error);
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error answering that." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full mt-10 mb-20">
            <div className="bg-gradient-to-br from-blue-950/20 to-zinc-950 p-1 rounded-3xl border border-blue-900/30 shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>

                <div className="bg-zinc-900/80 backdrop-blur-sm rounded-[1.3rem] p-6 min-h-[500px] flex flex-col">
                    <h3 className="text-xl font-extrabold mb-6 text-white flex items-center gap-3">
                        <MessageSquare size={24} className="text-blue-500" /> Ask AI Assistant
                    </h3>

                    {/* Chat Area */}
                    <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 max-h-[400px] custom-scrollbar">
                        {messages.map((msg, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {msg.role === 'assistant' && (
                                    <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                                        <Bot size={16} />
                                    </div>
                                )}

                                <div className={`
                                    p-4 rounded-2xl max-w-[80%] text-sm leading-relaxed
                                    ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white rounded-br-none'
                                        : 'bg-zinc-800 text-zinc-200 rounded-bl-none border border-zinc-700'}
                                `}>
                                    {msg.content}
                                </div>

                                {msg.role === 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center shrink-0">
                                        <User size={16} />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                        {loading && (
                            <div className="flex gap-3 justify-start">
                                <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                                    <Bot size={16} />
                                </div>
                                <div className="bg-zinc-800 p-4 rounded-2xl rounded-bl-none border border-zinc-700 flex items-center gap-2">
                                    <Loader2 className="w-4 h-4 animate-spin text-zinc-400" />
                                    <span className="text-xs text-zinc-400">Thinking...</span>
                                </div>
                            </div>
                        )}
                        <div ref={scrollRef} />
                    </div>

                    {/* Input Area */}
                    <form onSubmit={handleSend} className="relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question about the report..."
                            className="w-full bg-zinc-950/50 border border-zinc-700 rounded-xl py-4 pl-5 pr-14 text-zinc-200 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition placeholder:text-zinc-600"
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition disabled:opacity-50 disabled:hover:bg-blue-600"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
