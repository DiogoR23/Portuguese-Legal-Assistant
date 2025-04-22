import React, { useState, useRef, useEffect } from 'react';
import {
  Bars3Icon,
  PlusIcon,
  ArrowUpIcon,
} from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import UserMenu from '@/components/UserMenu';
import ThemeToggle from '@/components/ThemeToggle';
import {
  sendMessage,
  fetchUserConversations,
  fetchConversationMessages,
  createConversation
} from '@/services/api';
import TypingDots from '@/components/TypingDots';

const ChatPage = () => {
  const navigate = useNavigate();
  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(false);

  // Buscar histórico de conversas
  const fetchConversations = async () => {
    try {
      const res = await fetchUserConversations();
      setConversations(res.data);
    } catch (err) {
      console.error("Erro ao buscar conversas:", err);
    }
  };

  // Criar nova conversa
  const handleNewConversation = async () => {
    try {
      const res = await createConversation();
      setConversationId(res.data.id);
      setMessages([
        {
          role: 'assistant',
          content: 'Olá! Sou a Amel.IA. Em que posso ajudar-te com a legislação portuguesa hoje?',
        },
      ]);
      fetchConversations();
    } catch (err) {
      console.error("Erro ao criar nova conversa:", err);
    }
  };  

  // Carregar mensagens de conversa existente
  const AMELIA_WELCOME = {
    role: 'assistant',
    content: 'Olá! Sou a Amel.IA. Em que posso ajudar-te com a legislação portuguesa hoje?',
  };
  
  const loadConversation = async (id) => {
    try {
      const res = await fetchConversationMessages(id);
      setConversationId(id);
  
      const msgs = res.data;
  
      const isWelcomePresent =
        msgs.length > 0 &&
        msgs[0].role === 'assistant' &&
        msgs[0].content.includes('Em que posso ajudar-te');
  
      if (!isWelcomePresent) {
        setMessages([AMELIA_WELCOME, ...msgs]);
      } else {
        setMessages(msgs);
      }
  
    } catch (err) {
      console.error("Erro ao carregar mensagens:", err);
    }
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input.trim() };
    setInput('');
    setLoading(true);
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await sendMessage({
        message: userMessage.content,
        ...(conversationId && { conversation_id: conversationId }),
      });
      const { message: returnedMessages, conversation_id } = res.data;
      setConversationId(conversation_id);
      setMessages(prev => [...prev, ...returnedMessages]);
      fetchConversations(); // update titles, e.g., auto-titled on backend
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Erro ao obter resposta da IA. Tente novamente.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  // Efeitos
  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    const lineHeight = parseInt(getComputedStyle(textarea).lineHeight);
    const maxHeight = lineHeight * 5;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
    textarea.style.overflowY = textarea.scrollHeight > maxHeight ? 'auto' : 'hidden';
  }, [input]);

  return (
    <div className="h-screen overflow-hidden flex bg-background dark:bg-[#2a2a2a] text-foreground transition-colors duration-300">
      {/* Sidebar */}
      <aside
        className={`border-r border-gray-300 dark:border-gray-700 transition-all duration-300 ease-in-out ${sidebarOpen ? 'w-64' : 'w-0'} overflow-hidden bg-[#F2F2F2] dark:bg-[#1f1f1f]`}
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
              onClick={handleNewConversation}
              className="flex items-center gap-2 text-sm font-medium hover:bg-gray-300 dark:hover:bg-gray-600 p-2 rounded transition"
            >
              Nova Conversa
              <PlusIcon className="h-4 w-4" />
            </button>
          </div>

          <hr className="border-gray-300 dark:border-gray-700 mb-4 mt-2" />
          <div className='flex flex-col gap-2 overflow-y-auto'>
            {conversations.length === 0 ? (
              <p className='italic text-sm text-muted foreground'>Sem conversas ainda.</p>
            ) : (
              conversations.map((conv) => (
                <button
                  key={conv.id_conversation}
                  onClick={() => loadConversation(conv.id_conversation)}
                  className={`text-left text-sm px-3 py-2 rounded transition-all text-foreground 
                    ${conv.id === conversationId
                      ? 'bg-blue-600 text-white font-semibold'
                      : 'hover:bg-gray-300 dark:hover:bg-gray-700'
                    }`}
                >
                  {conv.title || `Conversa #${conv.id_conversation}`}
                </button>
              ))
            )}
          </div>
          <div className="mt-auto pt-6">
            <hr className="border-gray-300 dark:border-gray-700 mb-4" />
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Tema</span>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </aside>

      {/* Sidebar toggle (quando escondida) */}
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

        {/* Chat */}
        <main className="flex-1 bg-background dark:bg-[#2a2a2a] overflow-hidden">
          <div className="h-full px-4 py-6 flex justify-center">
            <div
              className="w-full max-w-4xl flex flex-col gap-4 overflow-y-auto rounded-md border border-transparent px-5 py-2 text-foreground bg-transparent leading-snug scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent"
              style={{ maxHeight: 'calc(100vh - 172px)' }}
            >
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`whitespace-pre-wrap break-words px-4 py-2 rounded-md ${
                    msg.role === 'user'
                      ? 'bg-blue-700 text-white self-end max-w-[80%]'
                      : 'text-foreground self-start max-w-[80%]'
                  }`}
                >
                  {msg.content}
                </div>
              ))}
              {loading && (
                <div className="self-start max-w-[80%]">
                  <TypingDots />
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </main>

        {/* Input */}
        <form onSubmit={handleSubmit} className="px-4 py-4 bg-background dark:bg-[#2a2a2a]">
          <div className="max-w-4xl mx-auto w-full">
            <div className="flex items-center justify-between rounded-[2rem] px-4 py-1.5 bg-background dark:bg-[#2a2a2a] border border-blue-600 shadow-md">
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
                style={{ maxHeight: '10rem', overflowY: 'auto' }}
              />
              <button
                type="submit"
                className={`ml-2 flex items-center justify-center w-9 h-9 rounded-full transition hover:opacity-80 shrink-0 ${
                  input.trim()
                    ? 'bg-blue-600 text-white hover:bg-blue-500 dark:bg-blue-600 dark:hover:bg-blue-500'
                    : 'bg-[#F2F2F2] text-black dark:bg-gray-700 dark:text-white cursor-not-allowed'
                }`}
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
