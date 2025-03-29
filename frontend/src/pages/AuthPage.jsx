// src/pages/LoginPage.jsx
import React from 'react';

const LoginPage = () => {
  return (
    <div className="min-h-screen flex">
      {/* Lado esquerdo - Logo */}
      <div className="w-1/2 bg-[#1e2a22] dark:bg-[#dbe7df] flex justify-center items-center">
        <h1 className="text-white dark:text-green-900 text-4xl font-extrabold underline">Amel.IA</h1>
      </div>

      {/* Lado direito - Formulário */}
      <div className="w-1/2 bg-[#1f1f1f] dark:bg-[#e9e9e9] flex justify-center items-center">
        <div className="w-[80%] max-w-md">
          <h2 className="text-white dark:text-black text-2xl font-bold mb-2">Iniciar Sessão</h2>
          <p className="text-gray-300 dark:text-gray-700 mb-6">Bem-vindo ao teu assistente jurídico</p>

          <form className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              className="w-full px-4 py-3 bg-[#3e3e3e] dark:bg-transparent border border-transparent dark:border-green-800 rounded-md text-white dark:text-black placeholder-gray-400 dark:placeholder-gray-600"
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full px-4 py-3 bg-[#3e3e3e] dark:bg-transparent border border-transparent dark:border-green-800 rounded-md text-white dark:text-black placeholder-gray-400 dark:placeholder-gray-600"
            />

            <div className="text-sm text-gray-400 dark:text-gray-600">
              Esqueceste-te da Password?{' '}
              <a href="#" className="text-white dark:text-green-800 underline">Altera-a Aqui.</a>
            </div>

            <button
              type="submit"
              className="w-full bg-green-700 text-white py-3 rounded-md hover:bg-green-800 transition"
            >
              Entrar
            </button>
          </form>

          <div className="mt-6 text-sm text-gray-400 dark:text-gray-600">
            Caso não tenha conta,{' '}
            <a href="#" className="text-white dark:text-green-800 underline">Registra-te Aqui.</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
