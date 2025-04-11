import React, { useState, useRef, useEffect } from 'react';
import {
  Bars3Icon,
  PlusIcon,
  ArrowUpIcon ,
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

  const [isAwaitingResponse, setIsAwaitingResponse] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isAwaitingResponse) return;

    const newMessage = { role: 'user', content: input.trim() };
    setMessages((prev) => [...prev, newMessage]);
    setInput('');
    setIsAwaitingResponse(true);

    setTimeout(() => {
      const fakeResponse = {
        role: 'assistant',
        content: 'Ainda estou a pensar... em breve terei uma resposta com base na DRE!',
      };
      setMessages((prev) => [...prev, fakeResponse]);
      setIsAwaitingResponse(false);
    }, 800);
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    const lineHeight = parseInt(getComputedStyle(textarea).lineHeight);
    const maxRows = 5;
    const maxHeight = lineHeight * maxRows;

    textarea.style.height = 'auto';
    const newHeight = Math.min(textarea.scrollHeight, maxHeight);
    textarea.style.height = `${newHeight}px`;
    textarea.style.overflowY = textarea.scrollHeight > maxHeight ? 'auto' : 'hidden';
  }, [input]);

const messagesEndRef = useRef(null);

useEffect(() => {
  if (messagesEndRef.current) {
    messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
  }
}, [messages]);

  return (
    <div className="h-screen overflow-hiden flex bg-background dark:bg-[#2a2a2a] text-foreground transition-colors duration-300">
      {/* Sidebar */}
      <aside
        className={`border-r border-gray-300 dark:border-gray-700 transition-all duration-300 ease-in-out ${
          sidebarOpen ? 'w-64' : 'w-0'
        } overflow-hidden bg-[#F2F2F2] dark:bg-[#1f1f1f]`}
      >
        <div className="h-full flex flex-col p-4">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition"
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
            <button
              onClick={() => navigate(0)}
              className="flex items-center gap-2 text-sm font-medium hover:bg-gray-200 dark:hover:bg-gray-700 p-2 rounded transition"
            >
              Nova Conversa
              <PlusIcon className="h-4 w-4" />
            </button>
          </div>

          <hr className="border-gray-300 dark:border-gray-700 mb-4 mt-2" />
          <p className="italic text-sm text-muted-foreground">Sem conversas ainda.</p>

          <div className="mt-auto pt-6">
            <hr className="border-gray-300 dark:border-gray-700 mb-4" />
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Tema</span>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </aside>

      {/* Botão para mostrar a sidebar quando está oculta */}
      {!sidebarOpen && (
        <button
          onClick={() => setSidebarOpen(true)}
          className="fixed top-4 left-4 z-50 p-2 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          <Bars3Icon className="h-6 w-6" />
        </button>
      )}

      {/* Main */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-0.5 border-gray-700 bg-background dark:bg-[#2a2a2a]">
          <div className="flex-1" />
          <h1 className="text-xl font-bold text-center text-primary flex-1">Amel.IA</h1>
          <div className="flex justify-end flex-1">
            <UserMenu />
          </div>
        </header>

        {/* Área de Chat */}
        <main className="flex-1 bg-background dark:bg-[#2a2a2a] overflow-hidden">
          <div className="h-full px-4 py-6 flex justify-center">
            <div
              className="w-full max-w-4xl flex flex-col gap-4 overflow-y-auto rounded-md border border-transparent px-5 py-2 text-foreground bg-transparent leading-snug scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent"
              style={{
                maxHeight: 'calc(100vh - 172px)',
                overflowY: 'auto',
              }}
            >
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`whitespace-pre-wrap break-words px-4 py-1 rounded-md ${
                    msg.role === 'user'
                      ? 'bg-blue-700 text-white self-end max-w-[80%]'
                      : 'text-foreground self-start max-w-[80%]'
                  }`}
                >
                  {msg.content}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </main>

        {/* Input */}
        <form onSubmit={handleSubmit} className="px-4 py-4 bg-background dark:bg-[#2a2a2a]">
          <div className="max-w-4xl mx-auto w-full">
            <div className="flex items-end justify-between rounded-[2rem] px-4 py-1.5 bg-bakground dark:bg-[#2a2a2a] border border-blue-600 shadow-md">

              {/* Textarea expansível e com scroll interno */}
              <textarea
                ref={textareaRef}
                rows={1}
                placeholder="Escreve a tua pergunta legal aqui..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                className="w-full resize-none bg-transparent text-black dark:text-white px-1 pr-3 focus:outline-none scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent"
                style={{
                  maxHeight: '10rem',
                  overflowY: 'auto',
                }}
              />

              {/* Botão de envio dentro do balão */}
              <button
                type="submit"
                className="ml-2 flex items-center justify-center w-9 h-9 bg-[#F2F2F2] text-black dark:bg-gray-700 dark:text-white rounded-full transition hover:opacity-80 shrink-0"
              >
                <ArrowUpIcon className="h-4 w-4" />
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
