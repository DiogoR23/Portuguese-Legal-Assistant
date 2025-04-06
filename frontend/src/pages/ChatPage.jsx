import React, { useState, useEffect, useRef } from 'react';
import {
  Bars3Icon,
  PlusIcon,
  PaperAirplaneIcon,
} from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import UserMenu from '@/components/UserMenu';
import ThemeToggle from '@/components/ThemeToggle';

const ChatPage = () => {
  const navigate = useNavigate();

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Olá! Sou a Amel.IA. Em que posso ajudar-te com a legislação portuguesa hoje?',
    },
  ]);
  const [input, setInput] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage = { role: 'user', content: input.trim() };
    setMessages((prev) => [...prev, newMessage]);

    const fakeResponse = {
      role: 'assistant',
      content: 'Ainda estou a pensar... em breve terei uma resposta com base na DRE!',
    };
    setTimeout(() => {
      setMessages((prev) => [...prev, fakeResponse]);
    }, 800);

    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
    }
  }, [input]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="min-h-screen flex bg-[#F8FAFC] dark:bg-[#1f1f1f] text-gray-900 dark:text-white transition-colors duration-300">
      {/* Sidebar */}
      <aside
        className={`transition-all duration-300 ease-in-out ${
          sidebarOpen ? 'w-64' : 'w-0'
        } overflow-hidden bg-white dark:bg-[#1a1a1a] border-r border-gray-300 dark:border-gray-700 flex flex-col`}
      >
        <div className="flex items-center justify-between px-4 py-3">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition"
          >
            <Bars3Icon className="h-5 w-5 text-gray-700 dark:text-gray-300" />
          </button>
          <button
            className="flex items-center gap-2 text-sm font-medium text-gray-900 dark:text-white px-3 py-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition"
          >
            <span>Nova Conversa</span>
            <PlusIcon className="h-4 w-4" />
          </button>
        </div>
        <hr className="mx-4 border-gray-400 dark:border-gray-700" />

        <div className="flex-1 px-4 py-6 text-sm italic text-blue-300 dark:text-blue-200">
          Sem conversas ainda.
        </div>

        <div className="mt-auto px-4 pb-4">
          <hr className="border-gray-400 dark:border-gray-700 mb-4" />
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Tema</span>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-4 border-b border-gray-300 dark:border-gray-700 bg-white dark:bg-[#1f1f1f]">
          <div className="w-1/3 flex items-center">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition"
              >
                <Bars3Icon className="h-6 w-6 text-gray-800 dark:text-gray-200" />
              </button>
            )}
          </div>
          <div className="w-1/3 text-center">
            <h1 className="text-2xl font-bold text-[#012A4A] dark:text-white">Amel.IA</h1>
          </div>
          <div className="w-1/3 flex justify-end">
            <UserMenu />
          </div>
        </header>

        {/* Chat Area */}
        <main className="flex-1 overflow-y-auto px-4 py-6 flex flex-col items-center bg-[#F8FAFC] dark:bg-[#1f1f1f]">
          <div className="w-full max-w-2xl flex flex-col gap-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`whitespace-pre-wrap break-words max-w-[80%] rounded-lg px-4 py-2 ${
                  msg.role === 'user'
                    ? 'bg-[#01497C] dark:bg-[#2A6F97] text-white self-end text-right shadow-md'
                    : 'text-black dark:text-white self-start text-left'
                }`}
              >
                {msg.content}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </main>

        {/* Input */}
        <form onSubmit={handleSubmit} className="px-4 py-4 border-t border-gray-300 dark:border-gray-700 bg-white dark:bg-[#1f1f1f]">
          <div className="max-w-4xl mx-auto flex items-end gap-2">
            <div className="flex-1">
              <div className="flex items-end bg-transparent border border-[#01497C] dark:border-[#2A6F97] rounded-3xl px-4 py-2 focus-within:ring-2 focus-within:ring-[#01497C] dark:focus-within:ring-[#2A6F97] transition">
                <textarea
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                  placeholder="Escreve a tua pergunta legal aqui..."
                  className="w-full resize-none bg-transparent text-white dark:text-white text-sm placeholder-gray-400 focus:outline-none max-h-[200px] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent"
                  style={{
                    lineHeight: '1.5rem',
                    maxHeight: '10rem',
                  }}
                />
                <button
                  type="submit"
                  className="ml-2 bg-[#01497C] hover:bg-[#2A6F97] text-white p-2 rounded-full flex items-center justify-center transition"
                >
                  <PaperAirplaneIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
