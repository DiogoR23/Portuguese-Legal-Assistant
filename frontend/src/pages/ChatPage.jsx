import React, { useState } from 'react';
import {
  Bars3Icon,
  XMarkIcon,
  ChatBubbleLeftEllipsisIcon,
  PlusIcon,
  QuestionMarkCircleIcon,
  PaperAirplaneIcon,
} from '@heroicons/react/24/outline';
import ThemeToggle from '@/components/ThemeToggle';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Olá! Sou a Amel.IA. Em que posso ajudar-te com a legislação portuguesa hoje?',
    },
  ]);
  const [input, setInput] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage = { role: 'user', content: input.trim() };
    setMessages((prev) => [...prev, newMessage]);

    // Simulação de resposta
    const fakeResponse = {
      role: 'assistant',
      content: '📚 Ainda estou a pensar... em breve terei uma resposta com base na DRE!',
    };
    setTimeout(() => {
      setMessages((prev) => [...prev, fakeResponse]);
    }, 800);

    setInput('');
  };

  return (
    <div className="min-h-screen flex bg-[#f4f4f4] dark:bg-[#1f1f1f] text-gray-900 dark:text-white">

      {/* Sidebar */}
      {sidebarOpen && (
        <aside className="w-64 bg-white dark:bg-[#1a1a1a] border-r border-gray-300 dark:border-gray-700 p-4 flex flex-col transition-all duration-300">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold">Menu</h2>
            <button onClick={() => setSidebarOpen(false)}>
              <XMarkIcon className="h-6 w-6 text-gray-700 dark:text-gray-300" />
            </button>
          </div>

          <nav className="space-y-3 text-sm">
            <button className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-green-100 dark:hover:bg-green-800 w-full text-left">
              <ChatBubbleLeftEllipsisIcon className="h-5 w-5" />
              Histórico
            </button>
            <button className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-green-100 dark:hover:bg-green-800 w-full text-left">
              <PlusIcon className="h-5 w-5" />
              Nova conversa
            </button>
            <button className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-green-100 dark:hover:bg-green-800 w-full text-left">
              <QuestionMarkCircleIcon className="h-5 w-5" />
              Ajuda
            </button>
          </nav>
        </aside>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-4 border-b border-gray-300 dark:border-gray-700 bg-white dark:bg-[#1f1f1f]">
          <div className="flex items-center gap-4">
            {!sidebarOpen && (
              <button onClick={() => setSidebarOpen(true)}>
                <Bars3Icon className="h-6 w-6 text-gray-800 dark:text-gray-200" />
              </button>
            )}
            <h1
              className="text-2xl font-bold cursor-pointer hover:underline"
              onClick={() => location.href = '/'}
            >
              Amel.IA
            </h1>
          </div>
          <ThemeToggle />
        </header>

        {/* Chat Area */}
        <main className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`max-w-xl px-4 py-3 rounded-md ${
                msg.role === 'user'
                  ? 'bg-green-100 dark:bg-green-900 ml-auto text-right'
                  : 'bg-gray-200 dark:bg-gray-700 text-left'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          ))}
        </main>

        {/* Input */}
        <form
          onSubmit={handleSubmit}
          className="p-4 border-t border-gray-300 dark:border-gray-700 bg-white dark:bg-[#1f1f1f] flex gap-2"
        >
          <input
            type="text"
            placeholder="Escreve a tua pergunta legal aqui..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 px-4 py-2 rounded-md border border-green-800 dark:bg-transparent dark:text-white focus:outline-none"
          />
          <button
            type="submit"
            className="bg-green-700 hover:bg-green-800 text-white px-4 py-2 rounded-md flex items-center justify-center transition"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
