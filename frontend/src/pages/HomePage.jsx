import React from 'react';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '@/components/ThemeToggle';

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <>
        <ThemeToggle />
        <div className="min-h-screen bg-[#f4f4f4] dark:bg-[#1f1f1f] text-gray-900 dark:text-white px-6 py-10">
            {/* Hero */}
            <section className="text-center max-w-4xl mx-auto mb-16">
            <h1 className="text-5xl font-extrabold mb-4">Amel.IA - O teu Assistente Jurídico Inteligente</h1>
            <p className="text-xl text-gray-700 dark:text-gray-400 max-w-2xl mx-auto">
                A primeira IA especializada em leis portuguesas, disponível 24/7 para responder às tuas dúvidas jurídicas com base no Diário da República.
            </p>
            <div className="mt-8 flex justify-center gap-4">
                <button
                onClick={() => navigate('/login')}
                className="bg-green-700 text-white px-6 py-3 rounded-md hover:bg-green-800 transition"
                >
                Iniciar Sessão
                </button>
                <button
                onClick={() => navigate('/register')}
                className="bg-gray-200 text-green-900 px-6 py-3 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 transition"
                >
                Criar Conta
                </button>
            </div>
            </section>

            {/* Sobre */}
            <section className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-3xl font-semibold text-green-800 dark:text-green-400 mb-4">Sobre a Amel.IA</h2>
            <p className="text-gray-700 dark:text-gray-300">
                Amel.IA é um chatbot jurídico construído com tecnologia de ponta em IA generativa.
                Utiliza um modelo LLM especializado através de <strong>RAG (Retrieval-Augmented Generation)</strong>, o que lhe permite
                aceder a legislação portuguesa atualizada, diretamente da <strong>DRE - Diário da República Eletrónico</strong>.
            </p>
            </section>

            {/* Como Funciona */}
            <section className="bg-green-50 dark:bg-green-900 py-12 rounded-md shadow-inner">
            <div className="max-w-4xl mx-auto px-6 text-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">Como Funciona?</h2>
                <div className="grid md:grid-cols-3 gap-8 text-left">
                <div>
                    <h3 className="text-lg font-semibold text-green-800 dark:text-green-300 mb-2">1. Pergunta à IA</h3>
                    <p className="text-gray-700 dark:text-gray-300">
                    Introduz a tua dúvida legal, de forma simples e direta.
                    </p>
                </div>
                <div>
                    <h3 className="text-lg font-semibold text-green-800 dark:text-green-300 mb-2">2. A IA pesquisa na legislação</h3>
                    <p className="text-gray-700 dark:text-gray-300">
                    Através de RAG, a IA encontra e analisa artigos da legislação relevante.
                    </p>
                </div>
                <div>
                    <h3 className="text-lg font-semibold text-green-800 dark:text-green-300 mb-2">3. Resposta clara e fundamentada</h3>
                    <p className="text-gray-700 dark:text-gray-300">
                    Recebes uma resposta baseada em fontes oficiais e atualizadas.
                    </p>
                </div>
                </div>
            </div>
            </section>

            {/* Benefícios */}
            <section className="max-w-4xl mx-auto text-center py-16 px-4">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Porquê usar a Amel.IA?</h2>
            <ul className="grid md:grid-cols-2 gap-6 text-left text-gray-700 dark:text-gray-300">
                <li>✅ Especializada em legislação portuguesa</li>
                <li>✅ Acesso instantâneo à informação legal</li>
                <li>✅ Respostas baseadas em documentos oficiais</li>
                <li>✅ Sem linguagem jurídica complexa</li>
                <li>✅ Disponível 24/7, sem burocracia</li>
                <li>✅ Ideal para estudantes, advogados e cidadãos curiosos</li>
            </ul>
            </section>

            {/* Call to Action final */}
            <div className="text-center mt-8">
            <h3 className="text-xl font-semibold mb-4">Pronto para começar?</h3>
            <div className="flex justify-center gap-4">
                <button
                onClick={() => navigate('/login')}
                className="bg-green-700 text-white px-6 py-3 rounded-md hover:bg-green-800 transition"
                >
                Iniciar Sessão
                </button>
                <button
                onClick={() => navigate('/register')}
                className="bg-gray-200 text-green-900 px-6 py-3 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 transition"
                >
                Criar Conta
                </button>
            </div>
            </div>
        </div>
        </>
    );
};

export default HomePage;
