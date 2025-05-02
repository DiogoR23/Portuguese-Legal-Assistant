import React, { useState, useRef, useEffect } from 'react';
import {
  Bars3Icon,
  PlusIcon,
  ArrowUpIcon,
  EllipsisVerticalIcon,
  StopCircleIcon,
} from '@heroicons/react/24/outline';
import {
  sendMessage,
  fetchUserConversations,
  fetchConversationMessages,
  createConversation,
  deleteConversation,
  updateConversation,
} from '@/services/api';
import TypingDots from '@/components/TypingDots';
import UserMenu from '@/components/UserMenu';
import ThemeToggle from '@/components/ThemeToggle';
import ConversationItemMenu from '@/components/ConversationItemMenu';

const ChatPage = () => {
  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState(null);
  const [showOptions, setShowOptions] = useState(null);
  const [menuPosition, setMenuPosition] = useState({ top: 0, left: 0 });
  const [editingTitle, setEditingTitle] = useState(null);
  const [newTitle, setNewTitle] = useState('');

  const AMELIA_WELCOME = {
    role: 'assistant',
    content: 'Olá! Sou a Amel.IA. Em que posso ajudar-te com a legislação portuguesa hoje?',
  };

  const fetchConversations = async () => {
    try {
      const res = await fetchUserConversations();
      setConversations(res.data);
    } catch (err) {
      console.error('Erro ao buscar conversas:', err);
    }
  };

  const handleNewConversation = async () => {
    const hasUserMessage = messages.some((m) => m.role === 'user');

    if (!hasUserMessage && messages.length > 0) {
      alert("Termina ou apaga esta conversa antes de iniciar uma nova.");
      return;
    }

    try {
      const res = await createConversation();
      setConversationId(res.data.id);
      setMessages([AMELIA_WELCOME]);
      fetchConversations();
    } catch (err) {
      console.error('Erro ao criar nova conversa:', err);
    }
  };

  const loadConversation = async (id) => {
    try {
      const res = await fetchConversationMessages(id);
      setConversationId(id);
      const msgs = res.data;
      const hasWelcome = msgs.some(
        (msg) => msg.role === 'assistant' && msg.content.includes('Em que posso ajudar-te')
      );
      setMessages(hasWelcome ? msgs : [AMELIA_WELCOME, ...msgs]);
    } catch (err) {
      console.error('Erro ao carregar mensagens:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const abortCtrl = new AbortController();
    setController(abortCtrl);

    const userMessage = { role: 'user', content: input.trim() };
    setInput('');
    setLoading(true);
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await sendMessage(
        {
          message: userMessage.content,
          ...(conversationId && { conversation_id: conversationId }),
        }, abortCtrl);

      const { message: returnedMessages, conversation_id } = res.data;
      setConversationId(conversation_id);
      setMessages((prev) => [...prev, ...returnedMessages]);
      fetchConversations();
    } catch (err) {
      if (err.name === 'CanceledError') {
        console.log('Requisição cancelada pelo utilizador.');
      } else {
        console.error('Erro ao enviar mensagem:', err);
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: 'Erro ao obter resposta da IA. Tente novamente.' },
        ]);
      }
    } finally {
      setLoading(false);
      setController(null);
    }
  };

  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id);
      fetchConversations();
      if (conversationId === id) {
        setConversationId(null);
        setMessages([AMELIA_WELCOME]);
      }
    } catch (err) {
      console.error('Erro ao apagar conversa:', err);
    }
  };

  const handleEditTitle = async (id) => {
    try {
      if (!newTitle.trim()) return;
      await updateConversation(id, newTitle.trim());
      fetchConversations();
      setEditingTitle(null);
      setNewTitle('');
    } catch (err) {
      console.error('Erro ao renomear conversa:', err);
    }
  };

  const handleOptionsClick = (e, id) => {
    e.stopPropagation();
    const rect = e.currentTarget.getBoundingClientRect();
    setMenuPosition({ top: rect.bottom + 4, left: rect.left });
    setShowOptions(id === showOptions ? null : id);
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (!conversationId && messages.length === 0) {
      setMessages([AMELIA_WELCOME]);
    }
  }, [conversationId]);

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
    <div className="h-screen overflow-hidden flex bg-background dark:bg-[#2a2a2a] text-foreground">
      {/* Sidebar */}
      <aside className={`transition-all ${sidebarOpen ? 'w-64' : 'w-0'} overflow-hidden border-r bg-[#F2F2F2] dark:bg-[#1f1f1f]`}>
        <div className="h-full flex flex-col p-4">
          <div className="flex items-center justify-between mb-4">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700">
              <Bars3Icon className="h-6 w-6" />
            </button>
            <button onClick={handleNewConversation} className="flex items-center gap-2 text-sm font-medium hover:bg-gray-200 dark:hover:bg-gray-700 p-2 rounded">
              Nova Conversa <PlusIcon className="h-4 w-4" />
            </button>
          </div>

          <hr className="border-gray-300 dark:border-gray-700 mb-4 mt-2" />
          <div className="flex flex-col gap-2 overflow-y-auto scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent hover:scrollbar-thumb-neutral-500">
            {conversations.length === 0 ? (
              <p className="italic text-sm text-muted-foreground">Sem conversas ainda.</p>
            ) : (
              conversations.map((conv) => (
                <div key={conv.id_conversation} className="relative group">
                  {editingTitle === conv.id_conversation ? (
                    <input
                      value={newTitle}
                      onChange={(e) => setNewTitle(e.target.value)}
                      className={`text-sm px-2 py-1 rounded w-full bg-gray-100 dark:bg-gray-700 text-black dark:text-white ${
                        conv.id_conversation === conversationId ? 'bg-blue-600 text-white' : ''
                      }`}
                      onBlur={() => setEditingTitle(null)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleEditTitle(conv.id_conversation);
                        }
                      }}
                      autoFocus
                    />
                  ) : (
                    <div className={`w-full px-3 py-2 text-sm rounded flex justify-between items-center group ${
                      conv.id_conversation === conversationId
                        ? 'bg-blue-600 text-white font-semibold'
                        : 'hover:bg-gray-300 dark:hover:bg-gray-700'
                    }`}>
                      <button onClick={() => loadConversation(conv.id_conversation)} className="flex-1 text-left truncate">
                        {conv.title || `Conversa #${conv.id_conversation}`}
                      </button>
                      <button
                        onClick={(e) => handleOptionsClick(e, conv.id_conversation)}
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <EllipsisVerticalIcon className="w-5 h-5" />
                      </button>
                    </div>
                  )}
                </div>
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

      {/* Floating menu */}
      {showOptions && (
        <ConversationItemMenu
          top={menuPosition.top}
          left={menuPosition.left}
          closeMenu={() => setShowOptions(null)}
          onRename={() => {
            setEditingTitle(showOptions);
            const conv = conversations.find(c => c.id_conversation === showOptions);
            setNewTitle(conv?.title || '');
            setShowOptions(null);
          }}
          onDelete={() => {
            handleDeleteConversation(showOptions);
            setShowOptions(null);
          }}
        />
      )}

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
        <header className="flex items-center justify-between px-4 py-1 border-gray-700 bg-background dark:bg-[#2a2a2a]">
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
            className="w-full max-w-4xl flex flex-col gap-4 overflow-y-auto px-5 py-2 leading-snug scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent hover:scrollbar-thumb-neutral-500"
            style={{ maxHeight: 'calc(100vh - 172px)' }}
          >
                {messages.map((msg, idx) => (
                  <div key={idx} className={`whitespace-pre-wrap break-words px-4 py-2 rounded-md ${
                    msg.role === 'user'
                      ? 'bg-blue-700 text-white self-end max-w-[80%]'
                      : 'text-foreground self-start max-w-[80%]'
                  }`}>
                    {msg.content}
                  </div>
                ))}
                {loading && <div className="self-start max-w-[80%]"><TypingDots /></div>}
                <div ref={messagesEndRef} />
            </div>
          </div>
        </main>

        {/* Input */}
        <form onSubmit={handleSubmit} className="px-4 py-4 bg-background dark:bg-[#2a2a2a]">
          <div className="max-w-4xl mx-auto w-full">
            <div className="flex items-center rounded-[2rem] px-4 py-1.5 border border-blue-600 shadow-md bg-background dark:bg-[#2a2a2a]">
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
              {loading && controller ? (
                <button
                  type="button"
                  onClick={() => {
                    controller.abort();
                    setLoading(false);
                    setController(null);
                  }}
                  className="ml-2 flex items-center justify-center w-9 h-9 rounded-full bg-red-600 text-white hover:bg-red-500 transition"
                >
                  <StopCircleIcon className="h-5 w-5" />
                </button>
              ) : (
                <button
                  type="submit"
                  className={`ml-2 flex items-center justify-center w-9 h-9 rounded-full transition ${
                    input.trim()
                      ? 'bg-blue-600 text-white hover:bg-blue-500'
                      : 'bg-[#F2F2F2] text-black dark:bg-gray-700 dark:text-white cursor-not-allowed'
                  }`}
                >
                  <ArrowUpIcon className="h-4 w-4" />
                </button>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
)};

export default ChatPage;