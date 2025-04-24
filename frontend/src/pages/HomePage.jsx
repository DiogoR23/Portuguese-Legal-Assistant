import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '@/components/ThemeToggle';
import { CheckBadgeIcon } from "@heroicons/react/24/outline";

const HomePage = () => {
  const navigate = useNavigate();
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('access');
    setToken(storedToken);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
    setToken(null);
    navigate('/login');
  };

  const username = localStorage.getItem('username');

  return (
    <div className="relative min-h-screen max-h-screen overflow-y-auto bg-white dark:bg-[#1f1f1f] text-black dark:text-white scrollbar-thin scrollbar-thumb-neutral-600 scrollbar-track-transparent hover:scollbar-thumb-neutral-500 transition-all duration-300 ease-in-out">
      <div className="absolute top-4 right-4 z-50">
        <ThemeToggle floating />
      </div>

      <div className="px-6 py-10">
        {/* Hero */}
        <section className="text-center max-w-4xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold mb-4 text-[#012A4A] dark:text-[#66bfff]">
            Amel.IA - O teu Assistente Jurídico Inteligente
          </h1>
          <p className="text-xl text-gray-800 dark:text-gray-300 max-w-2xl mx-auto">
            IA especializada em leis portuguesas, disponível 24/7 para responder às tuas dúvidas jurídicas com base no Diário da República (DRE).
          </p>
          <div className="mt-8 flex justify-center gap-4">
            {token ? (
              <>
                <button
                  onClick={() => navigate('/chat')}
                  className="bg-[#01497C] hover:bg-[#2A6F97] text-white px-6 py-3 rounded-md transition"
                >
                  Conversar com a Amel.IA
                </button>
                <button
                  onClick={handleLogout}
                  className="bg-red-100 text-red-700 px-6 py-3 rounded-md hover:bg-red-200 transition dark:bg-red-800 dark:text-white dark:hover:bg-red-700"
                >
                  Terminar Sessão
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => navigate('/login')}
                  className="bg-[#01497C] hover:bg-[#2A6F97] text-white px-6 py-3 rounded-md transition"
                >
                  Iniciar Sessão
                </button>
                <button
                  onClick={() => navigate('/register')}
                  className="bg-gray-100 text-black dark:bg-white dark:text-black px-6 py-3 rounded-md hover:bg-gray-300 dark:hover:bg-gray-200 transition"
                >
                  Criar Conta
                </button>
              </>
            )}
          </div>
        </section>

        {/* Sobre */}
        <section className="text-center max-w-3xl mx-auto mb-20">
          <h2 className="text-3xl font-semibold text-[#01497C] dark:text-[#66bfff] mb-4">
            Sobre a Amel.IA
          </h2>
          <p className="text-gray-800 dark:text-gray-300">
            Amel.IA é um chatbot jurídico construído com tecnologia de ponta em IA generativa.
            Utiliza um modelo LLM especializado através de <strong>RAG (Retrieval-Augmented Generation)</strong>,
            o que lhe permite aceder a legislação portuguesa atualizada, diretamente da <strong>DRE - Diário da República Eletrónico</strong>.
          </p>
        </section>

        {/* Como Funciona */}
        <section className="bg-[#E0ECF7] dark:bg-[#01497C] py-12 rounded-md shadow-inner transition-colors duration-300">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-2xl font-bold text-black dark:text-white mb-8">Como Funciona?</h2>
            <div className="grid md:grid-cols-3 gap-8 text-left text-black dark:text-white">
              <div>
                <h3 className="text-lg font-semibold mb-2">1. Pergunta à IA</h3>
                <p>Introduz a tua dúvida legal, de forma simples e direta.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">2. A IA pesquisa na legislação</h3>
                <p>Através de RAG, a IA encontra e analisa artigos da legislação relevante.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">3. Resposta clara e fundamentada</h3>
                <p>Recebes uma resposta baseada em fontes oficiais e atualizadas.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Benefícios */}
        <section className="max-w-4xl mx-auto text-center py-16 px-4">
          <h2 className="text-2xl font-bold text-black dark:text-white mb-6">Porquê usar a Amel.IA?</h2>
          <ul className="grid md:grid-cols-2 gap-6 text-left text-gray-800 dark:text-gray-300">
            {[
              'Especializada em legislação portuguesa',
              'Acesso instantâneo à informação legal',
              'Respostas baseadas em documentos oficiais',
              'Sem linguagem jurídica complexa',
              'Disponível 24/7, sem burocracia',
              'Ideal para estudantes, advogados e cidadãos curiosos',
            ].map((item, idx) => (
              <li
                key = {idx}
                className = "flex items-start gap-2"
              >
                <CheckBadgeIcon className="h-5 w-5 mt-1 text-[#01497C] dark:text-[#66bfff]" />
                <span> { item } </span>
              </li>
            ))}
          </ul>
        </section>

        {/* Call to Action final */}
        <div className="text-center mt-8">
          <h3 className="text-xl font-semibold mb-4 text-black dark:text-white">Pronto para começar?</h3>
          <div className="flex justify-center gap-4">
            {token ? (
              <button
                onClick={() => navigate('/chat')}
                className="bg-[#01497C] hover:bg-[#2A6F97] text-white px-6 py-3 rounded-md transition"
              >
                Conversar com a Amel.IA
              </button>
            ) : (
              <>
                <button
                  onClick={() => navigate('/login')}
                  className="bg-[#01497C] hover:bg-[#2A6F97] text-white px-6 py-3 rounded-md transition"
                >
                  Iniciar Sessão
                </button>
                <button
                  onClick={() => navigate('/register')}
                  className="bg-gray-100 text-black dark:bg-white dark:text-black px-6 py-3 rounded-md hover:bg-gray-300 dark:hover:bg-gray-200 transition"
                >
                  Criar Conta
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;